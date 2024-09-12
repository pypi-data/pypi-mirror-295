import json
from datetime import date, datetime, timezone
from typing import Any, Dict, Optional, Union
from urllib.parse import parse_qs, urlparse

import aiohttp
import dateutil.parser
import requests

from airfold_common._pydantic import BaseModel

BS = "\\"
must_escape = (BS, "'", "`")


def format_str(value: str):
    return f"'{escape_str(value)}'"


def escape_str(value: str):
    return "".join(f"{BS}{c}" if c in must_escape else c for c in value)


def quote_identifier(identifier: str):
    first_char = identifier[0]
    if first_char in ("`", '"') and identifier[-1] == first_char:
        # Identifier is already quoted, assume that it's valid
        return identifier
    return f"`{escape_str(identifier)}`"


RESPONSE_MAX_SIZE = 1024 * 1024 * 4
TOO_LARGE = f"Response exceeds maximum size: {RESPONSE_MAX_SIZE//1024//1024} MB"


def default_port(interface: str, secure: bool):
    if interface.startswith("http"):
        return 8443 if secure else 8123
    raise ValueError("Unrecognized ClickHouse interface")


def create_qs(params: dict[str, str]) -> dict[str, str]:
    return dict([("param_" + k, v) for k, v in params.items()])


DEFAULT_SETTINGS = {
    "max_execution_time": "28.5",
}


class PushResult(BaseModel):
    error: str | None = None
    query_id: str


class ChResponse:
    def __init__(self, body: Any, headers: Optional[Dict[str, str]] = None, status_code: int = 200):
        self.body = body
        self.headers = headers or {}
        self.status_code = status_code


class ChClientError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ChClient:
    def __init__(
        self,
        host: str | None = None,
        username: str | None = None,
        password: str = "",
        database: str = "__default__",
        interface: Optional[str] = None,
        port: int = 0,
        secure: Union[bool, str] = False,
        dsn: Optional[str] = None,
        app_name: Optional[str] = None,
        comment: Optional[str] = None,
        cluster: Optional[str] = None,
        **kwargs,
    ):
        use_tls = str(secure).lower() == "true" or interface == "https" or (not interface and port in (443, 8443))
        if dsn:
            parsed = urlparse(dsn)
            username = username or parsed.username
            password = password or (parsed.password if parsed.password else password)
            host = host or parsed.hostname
            port = port or (parsed.port or 0)
            if parsed.path and (not database or database == "__default__"):
                database = parsed.path[1:].split("/")[0]
            database = database or parsed.path
            kwargs.update(dict(parse_qs(parsed.query)))
        if host:
            parsed = urlparse(host)
            if not parsed.hostname:
                parsed = urlparse(f"//{host}")
            username = username or parsed.username
            password = password or parsed.password or ""
            host = parsed.hostname or host
            port = port or parsed.port or 0
            interface = interface or parsed.scheme
        if not interface:
            interface = "https" if use_tls else "http"
        if not host:
            host = "localhost"
        port = port or default_port(interface, use_tls)
        if username is None and "user" in kwargs:
            username = kwargs.pop("user")
        if username is None and "user_name" in kwargs:
            username = kwargs.pop("user_name")
        if password and username is None:
            username = "default"
        self.interface = interface
        self.host = host
        self.port = port
        self.username = username or "default"
        self.password = password or ""
        self.database = database
        self.headers = {
            "X-ClickHouse-User": self.username,
            "X-ClickHouse-Key": self.password,
            "User-Agent": f"airfold/1.0 ({app_name or ''})",
        }
        self.comment = comment
        self.cluster = cluster

    @property
    def url(self):
        return f"{self.interface}://{self.host}:{self.port}"

    def _get_render_push_data_sql(self, database: str, table: str, wait: Optional[bool]) -> str:
        return f"""
        INSERT INTO `{database}`.`{table}`
        SETTINGS async_insert=1,
                 wait_for_async_insert={1 if wait else 0},
                 async_insert_busy_timeout_ms=1000,
                 date_time_input_format='best_effort',
                 input_format_force_null_for_omitted_fields=1,
                 input_format_null_as_default=0
        FORMAT JSONEachRow
        """

    def sync_push_data(self, database: str, table: str, body: bytes, wait: bool | None = False) -> PushResult:
        data = self._get_render_push_data_sql(database, table, wait)
        res = requests.post(self.url, headers=self.headers, data=(data.encode("utf-8") + body))
        res_data = res.text
        if res.status_code >= 400:
            return PushResult(error=res_data, query_id=res.headers["X-ClickHouse-Query-Id"])
        return PushResult(query_id=res.headers.get("X-ClickHouse-Query-Id"))

    async def push_data(self, database: str, table: str, body: bytes, wait: bool | None = False) -> PushResult:
        data = self._get_render_push_data_sql(database, table, wait)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=(data.encode("utf-8") + body)) as res:
                res_data = await res.text()
                if res.status >= 400:
                    return PushResult(error=res_data, query_id=res.headers["X-ClickHouse-Query-Id"])
                return PushResult(query_id=res.headers["X-ClickHouse-Query-Id"])

    async def check_fmt(self, schema: str, body: bytes) -> str | None:
        data = f"""
SELECT * FROM format(JSONEachRow, $400f17aa${schema}$400f17aa$, $d57c68fa${body.decode("utf-8")}$d57c68fa$) FORMAT Null
"""
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=data.encode("utf-8")) as res:
                res_data = await res.text()
                if res.status >= 400:
                    return res_data
                return None

    async def get_empty_row(self, schema: str) -> dict:
        data = f"""
SELECT * FROM format('JSONEachRow', $${schema}$$, $${{}}$$) FORMAT JSONEachRow
"""
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=data.encode("utf-8")) as res:
                res_data = await res.text()
                return json.loads(res_data)

    def sync_query(
        self, sql: str, params: dict[str, str], fmt: str = "JSONEachRow", settings: dict | None = None
    ) -> ChResponse:
        qs_params = create_qs(params)
        qs_params["database"] = self.database
        if self.comment:
            qs_params["log_comment"] = self.comment
        qs_params = {**qs_params, **DEFAULT_SETTINGS, **(settings or {})}
        headers = {**self.headers, "X-ClickHouse-Format": fmt}
        try:
            res = requests.post(self.url, headers=headers, data=sql, params=qs_params, stream=True)
            if res.status_code >= 400:
                return ChResponse(
                    status_code=res.status_code,
                    body=json.dumps({"error": res.text}),
                    headers={"Content-Type": "application/json"},
                )
            result = []
            total_size = 0
            for chunk in res.iter_content(chunk_size=None, decode_unicode=(not is_binary_format(fmt))):
                total_size += len(chunk)
                if total_size >= RESPONSE_MAX_SIZE:
                    return ChResponse(
                        status_code=413,
                        body=json.dumps({"error": TOO_LARGE}),
                        headers={"Content-Type": "application/json"},
                    )
                result.append(chunk)
            if not result:
                body: str | bytes = ""
            elif isinstance(result[0], bytes):
                body = b"".join(result)
            else:
                body = "".join(result)
            return ChResponse(status_code=200, body=body, headers={"Content-Type": get_data_content_type(fmt)})
        except requests.exceptions.RequestException as e:
            return ChResponse(
                status_code=500, body=json.dumps({"error": repr(e)}), headers={"Content-Type": "application/json"}
            )

    def command(self, sql: str, params: dict[str, str] | None = None, settings: dict | None = None) -> None:
        qs_params = create_qs(params) if params else {}
        if self.database:
            qs_params["database"] = self.database
        if self.comment:
            qs_params["log_comment"] = self.comment
        qs_params = {**qs_params, **DEFAULT_SETTINGS, **(settings or {})}
        res = requests.post(self.url, headers=self.headers, data=sql.encode(), params=qs_params, stream=True)
        if res.status_code != 200:
            raise ChClientError(f"Error executing SQL: {res.reason} {res.text}", res.status_code)

    def grant_role_privileges(self, role: str, privileges: list[str], target: str):
        return self.command(f"""GRANT {", ".join(privileges)} ON {target} TO "{role}" """)

    def revoke_role_privileges(self, role: str, privileges: list[str], target: str):
        return self.command(f"""REVOKE {", ".join(privileges)} ON {target} FROM "{role}" """)


def parse_datetime(dt: str, default: Optional[datetime] = None) -> datetime:
    res: datetime = default or datetime.now(tz=timezone.utc)
    if dt:
        try:
            res = dateutil.parser.parse(dt)
        except dateutil.parser.ParserError:
            pass
    if res.tzinfo is None:
        res = res.replace(tzinfo=timezone.utc)
    return res


def format_datetime(value: Any):
    return format_str(datetime_to_str(value))


def format_query_value(value: Any):
    if value is None:
        return "NULL"
    if isinstance(value, str):
        return format_str(value)
    if isinstance(value, date) or isinstance(value, datetime):
        return format_datetime(value)
    if isinstance(value, list):
        return f"[{', '.join(str(format_query_value(x)) for x in value)}]"
    if isinstance(value, tuple):
        return f"({', '.join(str(format_query_value(x)) for x in value)})"
    if isinstance(value, dict):
        return f"{{{dict_to_str(value)}}}"
    return value


def dict_to_str(value: dict):
    pairs = [str(format_query_value(k)) + ":" + str(format_query_value(v)) for k, v in value.items()]
    return f"{', '.join(pairs)}"


def datetime_to_str(value: Any) -> str:
    if isinstance(value, datetime):
        return f"{value.strftime('%Y-%m-%d %H:%M:%S')}"
    if isinstance(value, date):
        return f"{value.isoformat()}"
    return value


def get_data_content_type(fmt: str) -> str:
    if fmt == "JSON":
        return "application/json"
    elif fmt == "JSONEachRow":
        return "application/x-ndjson"
    return "text/plain; charset=utf-8"


def is_binary_format(fmt: str) -> bool:
    if fmt in ["Native", "Parquet", "Arrow", "ArrowStream"]:
        return True
    return False
