import asyncio
import logging
import re
from contextlib import asynccontextmanager
from functools import reduce
from itertools import chain
from operator import itemgetter
from typing import Any, Callable, Coroutine, Iterable, NamedTuple, Optional, overload

import oracledb
import polars as pl
from asyncache import cached
from cachetools import LRUCache


def remove_null_columns(df: pl.DataFrame) -> pl.DataFrame:
    not_null_cols = filter(lambda x: x.null_count() != df.height, df)
    not_null_col_names = map(lambda x: x.name, not_null_cols)
    df = df.select(not_null_col_names)
    return df


oracledb.defaults.fetch_lobs = False  # type: ignore

ORACLE_TYPES_MAPPING = {
    "number": "SYS.ODCINUMBERLIST",
    "string": "SYS.ODCIVARCHAR2LIST",
    "bytes": "SYS.ODCIRAWLIST",
    "date": "SYS.ODCIDATELIST",
}


class ListReplacements(NamedTuple):
    query: str
    new_kwargs: dict[str, Any]


POLARS_TO_ORACLE_TYPES = {
    pl.Utf8: "string",
    pl.String: "string",
    pl.Int16: "number",
    pl.Int32: "number",
    pl.Int64: "number",
    pl.UInt64: "number",
    pl.UInt32: "number",
    pl.UInt16: "number",
    pl.Int8: "number",
    pl.UInt8: "number",
    pl.Float64: "number",
    pl.Float32: "number",
    pl.Binary: "bytes",
    pl.Date: "date",
    pl.Datetime: "date",
}


def oracle_to_polars_list(column_name: str, polars_dtype):
    return pl.col(column_name).map_elements(
        oracledb.DbObject.aslist, return_dtype=pl.List(polars_dtype)
    )


@cached(cache=LRUCache(maxsize=4))
async def get_oracle_db_type(con: oracledb.AsyncConnection, oracle_type: str):
    return await con.gettype(oracle_type)


def oracle_arraytype(lst: pl.Series):
    polars_type = lst.dtype.base_type()
    oracle_type = POLARS_TO_ORACLE_TYPES[polars_type]
    oracle_db_arr_type = ORACLE_TYPES_MAPPING[oracle_type]

    return oracle_db_arr_type


async def python_list_to_oracle_array(con: oracledb.AsyncConnection, series: pl.Series):
    oracle_db_arr_type = oracle_arraytype(series)
    oracle_db_arr_type = await get_oracle_db_type(con, oracle_db_arr_type)
    return oracle_db_arr_type.newobject(series)  # type: ignore


def replace_query_list(query: str, list_key: str) -> str:
    return query.replace(f":{list_key}", f"(SELECT * FROM TABLE(:{list_key}))")


def replace_query_lists(query: str, list_keys: Iterable[str]) -> str:
    return reduce(replace_query_list, list_keys, query)


async def replace_lists_and_query(
    con: oracledb.AsyncConnection, query: str, kwargs: dict[str, Any]
) -> ListReplacements:
    list_kwargs = filter(lambda item: isinstance(item[1], pl.Series), kwargs.items())
    non_list_kwargs = filter(
        lambda item: not isinstance(item[1], pl.Series), kwargs.items()
    )
    list_kwargs = list(list_kwargs)

    list_keys: map[str] = map(itemgetter(0), list_kwargs)
    query = replace_query_lists(query, list_keys)

    list_kwargs = [
        (item[0], await python_list_to_oracle_array(con, item[1]))
        for item in list_kwargs
    ]

    new_kwargs = chain(non_list_kwargs, list_kwargs)
    new_kwargs = dict(new_kwargs)

    return ListReplacements(query, new_kwargs)


async def replace_lists(con: oracledb.AsyncConnection, kwargs: dict[str, Any]):
    list_kwargs = filter(lambda item: isinstance(item[1], pl.Series), kwargs.items())
    list_kwargs = [
        (item[0], await python_list_to_oracle_array(con, item[1]))
        for item in list_kwargs
    ]
    kwargs.update(list_kwargs)
    return kwargs


LIMIT_REGEX = re.compile(r"LIMIT\s+(\d+)", re.IGNORECASE)


def limit_replacement(match: re.Match):
    return f"FETCH NEXT {match.group(1)} ROWS ONLY"


def replace_limit_sql(query: str) -> str:
    return LIMIT_REGEX.sub(limit_replacement, query)


async def cursor_to_df(cursor: oracledb.AsyncCursor, to_lower: bool) -> pl.DataFrame:
    columns = map(itemgetter(0), cursor.description)
    data = await cursor.fetchall()
    if to_lower:
        columns = map(str.lower, columns)
    columns = list(columns)
    cursor.close()
    return pl.DataFrame(data, schema=columns, orient="row")


class ReturningClauseInjection(NamedTuple):
    sql_with_returning: str
    cursor_returns: dict[str, oracledb.Var]
    cursor_to_col_names: dict[str, str]
    rowcount: int

    def collect(self):
        return_dict = {
            k: list(map(v.getvalue, range(self.rowcount)))
            for k, v in self.cursor_returns.items()
        }
        return_df = pl.DataFrame(return_dict)
        return_df = return_df.explode(pl.all())
        return_df = return_df.rename(self.cursor_to_col_names)
        return return_df

    @staticmethod
    def from_mutation(
        cursor: oracledb.AsyncCursor,
        df: pl.DataFrame,
        original_sql: str,
        return_schema: dict[str, type],
    ) -> "ReturningClauseInjection":
        rowcount = df.height

        cursor_returns = {
            f"{return_col}_return_cursor": cursor.var(
                typ=return_type, arraysize=rowcount
            )
            for return_col, return_type in return_schema.items()
        }
        column_names_to_cursor_names = dict(
            zip(cursor_returns.keys(), return_schema.keys())
        )
        cols_sql = ", ".join(return_schema.keys())
        return_cursor_placeholders = map(lambda x: f":{x}", cursor_returns.keys())
        return_cursor_placeholders_sql = ", ".join(return_cursor_placeholders)
        return_sql = f"RETURNING {cols_sql} INTO {return_cursor_placeholders_sql}"
        original_sql = f"{original_sql}\t{return_sql}"
        cursor.setinputsizes(**cursor_returns)
        return ReturningClauseInjection(
            original_sql,
            cursor_returns,
            column_names_to_cursor_names,
            rowcount,
        )


async def oracle_fetch(
    conn: oracledb.AsyncConnection,
    query: str,
    *,
    schema_overrides: Optional[dict] = None,
    to_lower: bool = True,
    **kwargs,
) -> pl.DataFrame:
    query, kwargs = await replace_lists_and_query(conn, query, kwargs)
    query = replace_limit_sql(query)

    with conn.cursor() as cursor:
        await cursor.execute(query, **kwargs)
        data = await cursor.fetchall()

        columns = map(itemgetter(0), cursor.description)
        if to_lower:
            columns = map(str.lower, columns)
        columns = list(columns)

    return pl.DataFrame(
        data,
        schema=columns,
        orient="row",
        schema_overrides=schema_overrides,
        infer_schema_length=len(data),
    )


async def oracle_call_sproc(
    conn: oracledb.AsyncConnection,
    proc: str,
    *,
    out_keys: dict[str, Any],
    to_lower: bool = True,
    **kwargs,
) -> dict[str, Any]:
    kwargs = await replace_lists(conn, kwargs)

    with conn.cursor() as cursor:
        out_vals = map(cursor.var, out_keys.values())  # type: ignore
        out_vals = list(out_vals)
        out_dict = zip(out_keys.keys(), out_vals)
        kwargs.update(out_dict)

        await cursor.callproc(proc, keyword_parameters=kwargs)

        out_results = map(oracledb.Var.getvalue, out_vals)
        out_results = map(
            lambda x: cursor_to_df(x, to_lower)
            if isinstance(x, oracledb.AsyncCursor)
            else x,
            out_results,
        )
        out_results = zip(out_keys.keys(), out_results)
        out_results = dict(out_results)
    coros_dict = filter(lambda x: isinstance(x[1], Coroutine), out_results.items())
    coros_dict = dict(coros_dict)

    results = await asyncio.gather(*coros_dict.values())  # type: ignore

    coros_dict = zip(coros_dict.keys(), results)
    out_results.update(coros_dict)
    return out_results


def gen_set_sql(col: str, *, include_nulls: bool = False):
    if include_nulls:
        return f"{col} = :{col}"
    return f"{col} = COALESCE(:{col}, {col})"


def named_to_numbered_params(df: pl.DataFrame, query: str):
    for i, col in enumerate(df.columns, 1):
        query = query.replace(f":{col}", f":{i}")
    return query


def get_inject_sql(key: str, value: str):
    return f"{key} = {value}"


UPDATE_BREADCRUMB = (
    ", UPDATE_TS = SYSDATE, UPDATE_USER = SYS_CONTEXT('USERENV', 'OS_USER')"
)


async def update_many(
    conn: oracledb.AsyncConnection,
    df: pl.DataFrame,
    table: str,
    *,
    pkey_cols: set[str],
    include_nulls: bool = False,
    logger: logging.Logger,
    leave_update_breadcrumb: bool = True,
    sql_injections: Optional[dict[str, str]] = None,
    return_schema: Optional[dict[str, type]] = None,
):
    df = remove_null_columns(df)
    df_cols = set(df.columns)
    non_pkey_cols = df_cols.difference(pkey_cols)

    set_sqls = map(
        lambda x: gen_set_sql(x, include_nulls=include_nulls),
        non_pkey_cols,
    )

    inject_sqls = (
        map(get_inject_sql, sql_injections.keys(), sql_injections.values())
        if sql_injections
        else list[str]()
    )
    set_sqls = chain(set_sqls, inject_sqls)
    set_sql = ", ".join(set_sqls)

    where_sqls = map(lambda x: gen_set_sql(x, include_nulls=True), pkey_cols)
    where_sql = " AND ".join(where_sqls)
    update_breadcrumb = UPDATE_BREADCRUMB if leave_update_breadcrumb else ""
    update_sql = f"""--sql
        UPDATE {table}
        SET {set_sql}{update_breadcrumb}
        WHERE {where_sql}
    """

    rows = df.to_dicts()

    with conn.cursor() as cursor:
        returning_state = None
        if return_schema is not None:
            returning_state = ReturningClauseInjection.from_mutation(
                cursor, df, update_sql, return_schema
            )
            update_sql = returning_state.sql_with_returning

        logger.debug(f"Updating Oracle with:\n{update_sql}\nwith df:\n{df}")
        await cursor.executemany(update_sql, rows)
        logger.debug(rows)
        if returning_state is not None:
            return returning_state.collect()
    return None


async def insert_many(
    conn: oracledb.AsyncConnection,
    df: pl.DataFrame,
    table: str,
    *,
    return_schema: Optional[dict[str, type]],
    logger: logging.Logger,
):
    df = remove_null_columns(df)
    columns_sql = ", ".join(df.columns)
    values_sqls = map(lambda col: f":{col}", df.columns)
    values_sql = ", ".join(values_sqls)

    insert_sql = f"""--sql
        INSERT INTO {table} ({columns_sql})
        VALUES ({values_sql})
    """

    rows = df.to_dicts()
    with conn.cursor() as cursor:
        returning_state = None
        if return_schema is not None:
            returning_state = ReturningClauseInjection.from_mutation(
                cursor, df, insert_sql, return_schema
            )
            insert_sql = returning_state.sql_with_returning

        logger.debug(f"Inserting into Oracle with:\n{insert_sql}\nwith df:\n{df}")
        await cursor.executemany(insert_sql, rows)
        if returning_state is not None:
            return returning_state.collect()
    return None


async def delete_many(
    conn: oracledb.AsyncConnection,
    df: pl.DataFrame,
    table: str,
    *,
    return_schema: Optional[dict[str, type]],
    logger: logging.Logger,
):
    df_cols = set(df.columns)

    where_sqls = map(lambda x: gen_set_sql(x, include_nulls=True), df_cols)
    where_sql = " AND ".join(where_sqls)

    delete_sql = f"""--sql
        DELETE FROM {table}
        WHERE {where_sql}
    """
    rows = df.to_dicts()
    with conn.cursor() as cursor:
        returning_state = None
        if return_schema is not None:
            returning_state = ReturningClauseInjection.from_mutation(
                cursor, df, delete_sql, return_schema
            )
            delete_sql = returning_state.sql_with_returning

        logger.debug(f"Deleting from Oracle with:\n{delete_sql}\nwith df:\n{df}")
        await cursor.executemany(delete_sql, rows)
        if returning_state is not None:
            return returning_state.collect()
    return None


class PoolWrapper:
    pool_factory: Callable[..., oracledb.AsyncConnectionPool]
    pool: Optional[oracledb.AsyncConnectionPool]
    logger: logging.Logger

    def __init__(
        self,
        pool_factory: Callable[..., oracledb.AsyncConnectionPool],
        logger: Optional[logging.Logger],
    ):
        self.pool_factory = pool_factory
        self.pool = None
        self.logger = logger or logging.getLogger("oracle")

    @asynccontextmanager
    async def acquire(self):
        if self.pool is None:
            self.pool = self.pool_factory()
        async with self.pool.acquire() as conn:
            yield conn

    @asynccontextmanager
    async def start_transaction(self):
        async with self.acquire() as conn:
            yield ConnWrapper(conn, self.logger)
            if conn.transaction_in_progress:
                await conn.commit()

    async def close(self):
        if self.pool:
            await self.pool.close(force=True)

    async def fetch(
        self,
        query: str,
        *,
        schema_overrides: Optional[dict] = None,
        to_lower: bool = True,
        **kwargs,
    ) -> pl.DataFrame:
        async with self.acquire() as conn:
            return await oracle_fetch(
                conn,
                query,
                schema_overrides=schema_overrides,
                to_lower=to_lower,
                **kwargs,
            )

    async def fetch_proc(
        self,
        proc: str,
        *,
        out_keys: dict[str, Any],
        to_lower: bool = True,
        **kwargs,
    ) -> dict[str, Any]:
        async with self.acquire() as conn:
            return await oracle_call_sproc(
                conn, proc, out_keys=out_keys, to_lower=to_lower, **kwargs
            )

    @overload
    async def delete_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        return_schema: dict[str, type],
    ) -> pl.DataFrame: ...

    @overload
    async def delete_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        return_schema: None = None,
    ) -> None: ...

    async def delete_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        return_schema: Optional[dict[str, type]] = None,
    ):
        async with self.acquire() as conn:
            conn.autocommit = True
            res = await delete_many(
                conn, df, table, return_schema=return_schema, logger=self.logger
            )
            conn.autocommit = False
        return res

    @overload
    async def update_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        pkey_cols: set[str],
        include_nulls: bool = False,
        leave_update_breadcrumb: bool = True,
        sql_injections: Optional[dict[str, str]] = None,
        return_schema: dict[str, type],
    ) -> pl.DataFrame: ...

    @overload
    async def update_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        pkey_cols: set[str],
        include_nulls: bool = False,
        leave_update_breadcrumb: bool = True,
        sql_injections: Optional[dict[str, str]] = None,
        return_schema: None = None,
    ) -> None: ...

    async def update_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        pkey_cols: set[str],
        include_nulls: bool = False,
        leave_update_breadcrumb: bool = True,
        sql_injections: Optional[dict[str, str]] = None,
        return_schema: Optional[dict[str, type]] = None,
    ):
        async with self.acquire() as conn:
            conn.autocommit = True
            res = await update_many(
                conn,
                df,
                table,
                pkey_cols=pkey_cols,
                include_nulls=include_nulls,
                leave_update_breadcrumb=leave_update_breadcrumb,
                sql_injections=sql_injections,
                return_schema=return_schema,
                logger=self.logger,
            )
            conn.autocommit = False
        return res

    @overload
    async def insert_many(
        self, df: pl.DataFrame, table: str, *, return_schema: dict[str, type]
    ) -> pl.DataFrame: ...

    @overload
    async def insert_many(
        self, df: pl.DataFrame, table: str, *, return_schema: None = None
    ) -> None: ...

    async def insert_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        return_schema: Optional[dict[str, type]] = None,
    ):
        async with self.acquire() as conn:
            conn.autocommit = True
            res = await insert_many(
                conn, df, table, return_schema=return_schema, logger=self.logger
            )
            conn.autocommit = False
        return res


class ConnWrapper:
    conn: oracledb.AsyncConnection
    logger: logging.Logger

    def __init__(self, conn: oracledb.AsyncConnection, logger: logging.Logger):
        self.conn = conn
        self.logger = logger

    async def fetch(
        self,
        query: str,
        *,
        schema_overrides: Optional[dict] = None,
        to_lower: bool = True,
        **kwargs,
    ) -> pl.DataFrame:
        return await oracle_fetch(
            self.conn,
            query,
            schema_overrides=schema_overrides,
            to_lower=to_lower,
            **kwargs,
        )

    async def fetch_proc(
        self,
        proc: str,
        *,
        out_keys: dict[str, Any],
        to_lower: bool = True,
        **kwargs,
    ) -> dict[str, Any]:
        return await oracle_call_sproc(
            self.conn,
            proc,
            to_lower=to_lower,
            out_keys=out_keys,
            **kwargs,
        )

    @overload
    async def update_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        pkey_cols: set[str],
        include_nulls: bool = False,
        leave_update_breadcrumb: bool = True,
        sql_injections: Optional[dict[str, str]] = None,
        return_schema: dict[str, type],
    ) -> pl.DataFrame: ...

    @overload
    async def update_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        pkey_cols: set[str],
        include_nulls: bool = False,
        leave_update_breadcrumb: bool = True,
        sql_injections: Optional[dict[str, str]] = None,
        return_schema: None = None,
    ) -> None: ...

    async def update_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        pkey_cols: set[str],
        include_nulls: bool = False,
        sql_injections: Optional[dict[str, str]] = None,
        leave_update_breadcrumb: bool = True,
        return_schema: Optional[dict[str, type]] = None,
    ):
        return await update_many(
            self.conn,
            df,
            table,
            pkey_cols=pkey_cols,
            include_nulls=include_nulls,
            sql_injections=sql_injections,
            leave_update_breadcrumb=leave_update_breadcrumb,
            return_schema=return_schema,
            logger=self.logger,
        )

    @overload
    async def insert_many(
        self, df: pl.DataFrame, table: str, *, return_schema: dict[str, type]
    ) -> pl.DataFrame: ...

    @overload
    async def insert_many(
        self, df: pl.DataFrame, table: str, *, return_schema: None = None
    ) -> None: ...

    async def insert_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        return_schema: Optional[dict[str, type]] = None,
    ):
        return await insert_many(
            self.conn, df, table, return_schema=return_schema, logger=self.logger
        )

    @overload
    async def delete_many(
        self, df: pl.DataFrame, table: str, *, return_schema: dict[str, type]
    ) -> pl.DataFrame: ...

    @overload
    async def delete_many(
        self, df: pl.DataFrame, table: str, *, return_schema: None = None
    ) -> None: ...

    async def delete_many(
        self,
        df: pl.DataFrame,
        table: str,
        *,
        return_schema: Optional[dict[str, type]] = None,
    ):
        return await delete_many(
            self.conn, df, table, return_schema=return_schema, logger=self.logger
        )

    async def commit(self):
        await self.conn.commit()
        return self

    async def rollback(self):
        await self.conn.rollback()
        return self
