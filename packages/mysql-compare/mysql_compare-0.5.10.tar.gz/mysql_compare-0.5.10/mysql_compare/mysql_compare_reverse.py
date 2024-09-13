import concurrent.futures
import datetime
import json
import logging
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal

from mysql.connector import MySQLConnection, connect


@dataclass
class ComparisonTask:
    batch_id: int
    source_rows: list[dict]
    different: list[dict]


def hash_dict(d):
    return frozenset(d.items())


def find_missing_in_b(a, b):
    b_hashes = {hash_dict(d) for d in b}

    missing_in_b = [d for d in a if hash_dict(d) not in b_hashes]

    return missing_in_b


def get_table_rows_by_key(con: MySQLConnection, database: str, table: str, diff_row: dict) -> dict:
    where_clause = " AND ".join([f"`{col}` = %s" for col in diff_row.keys()])

    params = diff_row.values()

    _stmt = f"SELECT 1 FROM `{database}`.`{table}` WHERE {where_clause}"

    print(_stmt, tuple(params))

    with con.cursor(buffered=True) as cur:
        cur.execute(_stmt, tuple(params))
        return cur.fetchone()


def delete_row_by_key(con: MySQLConnection, database: str, table: str, diff_row: dict) -> dict:
    where_clause = " AND ".join([f"`{col}` = %s" for col in diff_row.keys()])

    params = diff_row.values()

    _stmt = f"DELETE FROM `{database}`.`{table}` WHERE {where_clause}"

    print(_stmt, tuple(params))

    with con.cursor(buffered=True) as cur:
        cur.execute(_stmt, tuple(params))
    con.commit()


def get_table_rows_number(con: MySQLConnection, database: str, table: str) -> int:
    with con.cursor() as cur:
        cur.execute("SELECT table_rows FROM information_schema.tables WHERE table_schema = %s AND table_name = %s", (database, table))
        (rows,) = cur.fetchone()
        return rows


def get_table_structure(con: MySQLConnection, database: str, table: str) -> list[tuple[str, str]]:
    with con.cursor() as cur:
        cur.execute(
            "SELECT column_name, CAST(data_type as char(255)) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position",
            (database, table),
        )
        return cur.fetchall()


def get_table_keys(con: MySQLConnection, database: str, table: str):
    operation = """
        SELECT tis.index_name, titc.constraint_type, tic.column_name, tic.data_type
        FROM information_schema.table_constraints titc
        JOIN information_schema.statistics tis ON titc.table_schema = tis.table_schema AND titc.table_name = tis.table_name AND titc.constraint_name = tis.index_name
        JOIN information_schema.columns tic ON tis.table_schema = tic.table_schema AND tis.table_name = tic.table_name AND tis.column_name = tic.column_name
        WHERE titc.constraint_type IN ('PRIMARY KEY', 'UNIQUE')
        AND titc.table_schema = %s
        AND titc.table_name = %s
    """

    with con.cursor() as cur:
        cur.execute(operation, (database, table))
        rows = cur.fetchall()

    pkeys = [(row[2], row[3]) for row in rows if row[1] == "PRIMARY KEY"]
    ukeys = [(row[2], row[3]) for row in rows if row[1] == "UNIQUE" and row[0] == rows[0][0]]

    if not pkeys and not ukeys:
        raise Exception("does not have primary key or unique keys.")

    return pkeys, ukeys


def get_elapsed_time(st: float, ndigits=None) -> int | float:
    return round(time.time() - st, ndigits)


def extract_keyvals(row: dict, keys: list[tuple[str, str]]):
    _keys = [item[0] for item in keys]
    new_dict = {}
    for key in row:
        if key in _keys:
            new_dict[key] = row[key]

    return new_dict


def query_rows(con: MySQLConnection, query_statement: str, query_params) -> list[dict]:
    with con.cursor(dictionary=True, buffered=True) as cur:
        cur.execute(query_statement, tuple(query_params))
        return cur.fetchall()


class MysqlTableCompare:
    def __init__(
        self,
        src_dsn: dict,
        dst_dsn: dict,
        src_database: str,
        src_table: str,
        dst_database: str,
        dst_table: str,
        limit_size: int = 2000,
    ) -> None:
        self.source_dsn = src_dsn
        self.target_dsn = dst_dsn

        self.limit_size = limit_size

        self.src_database = src_database
        self.src_table = src_table
        self.dst_database = dst_database
        self.dst_table = dst_table

        self.compare_name: str = f"{self.src_database}.{self.src_table}"
        if self.src_database == self.dst_database and self.src_table != self.dst_table:
            self.compare_name += f".{self.dst_table}"
        elif self.src_database != self.dst_database:
            self.compare_name += f".{self.dst_database}.{self.dst_table}"

        self.different_file = f"{self.compare_name}.diff.log"

    def get_query_full_table_statement_params(self, database: str, table: str, ckpt_row: dict = None):
        _keyval = ckpt_row
        # select * from where 1 = 1 and ((a > xxx) or (a = xxx and b > yyy) or (a = xxx and b = yyy and c > zzz)) order by a,b,c limit checksize
        _key_colns = ", ".join([f"`{col[0]}`" for col in self.source_table_pkeys])

        _sel_cols = ", ".join([f"`{col[0]}`" for col in self.source_table_pkeys + self.source_table_ukeys])

        _order_cols = _key_colns or _sel_cols

        for _, column_type in self.source_table_pkeys:
            if column_type in ["int", "double", "char", "date", "decimal", "varchar", "bigint", "tinyint", "smallint", "datetime"]:
                pass
            else:
                raise ValueError(f"Data type: [{column_type}] is not supported yet.")

        where_conditions = []
        for end_idx in range(len(self.source_table_pkeys)):
            condition_parts = []
            for i, (column_name, _) in enumerate(self.source_table_pkeys[: end_idx + 1]):
                operator = ">" if i == end_idx else "="
                condition_parts.append(f"`{column_name}` {operator} %s")
            where_conditions.append(" and ".join(condition_parts))
        where_clause = "WHERE " + "(" + ") or (".join(where_conditions) + ")"

        statement_with_condition = f"SELECT {_sel_cols} FROM {database}.{table} {where_clause} ORDER BY {_order_cols} LIMIT {self.limit_size}"
        statement_without_condition = f"SELECT {_sel_cols} FROM {database}.{table} ORDER BY {_order_cols} LIMIT {self.limit_size}"

        _params: list = []
        if _keyval:
            for end_idx in range(len(self.source_table_pkeys)):
                for i, (column_name, _) in enumerate(self.source_table_pkeys[: end_idx + 1]):
                    _params.append(_keyval[column_name])

        statement = statement_with_condition if _params else statement_without_condition

        return statement, _params

    def compare_full_table(self, source_con: MySQLConnection, target_con: MySQLConnection):
        _keyval = None
        _processed_rows_number = 0
        batch_id = 1

        while True:
            query_statement_src, query_params_src = self.get_query_full_table_statement_params(self.src_database, self.src_table, _keyval)
            query_statement_dst, query_params_dst = self.get_query_full_table_statement_params(self.dst_database, self.dst_table, _keyval)

            self.logger.info(f"batch_id[{batch_id}] source query statment: '{query_statement_src}', params '{query_params_src}'")
            self.logger.info(f"batch_id[{batch_id}] target query statment: '{query_statement_dst}', params '{query_params_dst}'")

            source_rows = []
            target_rows = []
            diff_rows = []

            _start1 = time.time()

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                future_source = executor.submit(query_rows, source_con, query_statement_src, query_params_src)
                future_target = executor.submit(query_rows, target_con, query_statement_dst, query_params_dst)

                source_rows = future_source.result()
                target_rows = future_target.result()

            if len(target_rows) == 0:
                return

            _processed_rows_number += len(source_rows)

            diff_rows = find_missing_in_b(target_rows, source_rows)

            for diff_row in diff_rows:
                trow = get_table_rows_by_key(source_con, self.src_database, self.src_table, diff_row)
                print("dif frow", diff_row, trow)
                if trow is None:
                    delete_row_by_key(target_con, self.dst_database, self.dst_table, diff_row)
                    print(f"delete row {self.dst_database}.{self.dst_table} {diff_row}")

            _keyval = extract_keyvals(target_rows[-1], self.source_table_pkeys)

            processed_progress = round(_processed_rows_number / self.source_table_rows_number * 100, 2)
            self.logger.info(f"batch_id[{batch_id}] source rows: {len(source_rows)}, target rows: {len(target_rows)}.")
            self.logger.info(
                f"batch_id[{batch_id}] processed rows number: {_processed_rows_number}/{self.source_table_rows_number}, progress: {processed_progress}%, elapsed time: {get_elapsed_time(_start1, 2)}s."
            )
            batch_id += 1

    def run(self) -> None:
        self.logger = init_logger(self.compare_name)

        with connect(**self.source_dsn) as source_con, connect(**self.target_dsn) as target_con:
            source_table_struct: list[tuple[str, str]] = get_table_structure(source_con, self.src_database, self.src_table)
            target_table_struct: list[tuple[str, str]] = get_table_structure(target_con, self.dst_database, self.dst_table)

            self.logger.info(f"source table structure: {self.source_dsn} {self.src_database} {self.src_table} {source_table_struct}.")
            self.logger.info(f"target table structure: {self.target_dsn} {self.dst_database} {self.dst_table} {target_table_struct}.")

            table_struct_diff = set(source_table_struct) - set(target_table_struct)

            if not source_table_struct or table_struct_diff:
                raise Exception("source and target table structure diff.")

            self.logger.info("source and target table structure same.")

            self.source_table_pkeys, self.source_table_ukeys = get_table_keys(source_con, self.src_database, self.src_table)

            self.logger.info(f"source table primary keys: {self.source_table_pkeys}.")
            self.logger.info(f"source table unique keys: {self.source_table_ukeys}.")

            if len(self.source_table_pkeys) == 0 and len(self.source_table_ukeys) == 0:
                raise Exception("primary or unique not exists.")

            if len(self.source_table_pkeys) == 0 and len(self.source_table_ukeys) >= 1:
                self.source_table_pkeys = self.source_table_ukeys.copy()
                self.source_table_ukeys = []

            self.source_table_rows_number = max(1, get_table_rows_number(source_con, self.src_database, self.src_table))
            self.logger.info(f"source table rows number: {self.source_table_rows_number}.")

            self.compare_full_table(source_con, target_con)  # main


def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_tables(dsn):
    with connect(**dsn) as con:
        cur = con.cursor()
        cur.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('merchant_center_vela_v1') ORDER BY 1, 2")
        for db, tab in cur.fetchall():
            yield (db, tab)


source_dsn = {"host": "10.50.10.83", "port": 3310, "user": "ghost", "password": "54448hotINBOX", "time_zone": "+00:00"}
target_dsn = {"host": "10.50.10.83", "port": 3317, "user": "ghost", "password": "54448hotINBOX", "time_zone": "+00:00"}


def run_compare(db, tab):
    try:
        MysqlTableCompare(source_dsn, target_dsn, db, tab, db, tab, 50000).run()
    except Exception as e:
        print(f"error {db}.{tab} {e}")


if __name__ == "__main__":
    # docker rm -f tmp1
    # docker run -d --name tmp1 -v /opt/mysql-compare/reverse.bak:/opt --network host -w /opt python:3 sleep inf
    # docker exec -it tmp1 pip install mysql-connector-python==9.0.0
    #
    compare_success = 0
    parallel = 20

    with ProcessPoolExecutor(max_workers=parallel) as executor:
        future_to_task = {executor.submit(run_compare, src_db, src_tab): f"{src_db}.{src_tab}" for src_db, src_tab in get_tables(source_dsn)}

        for future in as_completed(future_to_task):
            task = future_to_task[future]
            compare_success += 1
            try:
                result = future.result()
            except Exception as e:
                print(f"{get_current_datetime()} {task} generated an exception: {e}")
            finally:
                print(f"{get_current_datetime()} compare progress: {compare_success}")

    print(f"{get_current_datetime()} compare all done.")
