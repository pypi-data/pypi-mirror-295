import inspect
import os
import psycopg2
import pandas as pd
from psycopg2 import sql
from typing import Any, Optional
import dotenv


class PostgresConnection:
    def __init__(
        self,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
    ):
        if os.path.isfile('.env'):
            dotenv.load_dotenv()

        self.host = os.environ['postgres_host'] if host is None else host
        self.username = os.environ['postgres_username'] if username is None else username
        self.password = os.environ['postgres_password'] if password is None else password
        self.database = os.environ['postgres_database'] if database is None else database

        if self.host is None or self.database is None or self.username is None or self.password is None:
            raise RuntimeError('No env. variable set or .env file given while one of the parameters is missing.')

        self.connection: Optional[Any] = None

    def __enter__(self):
        calling_function = inspect.stack()[2][3]

        self.connection = psycopg2.connect(
            host=self.host,
            dbname=self.database,
            user=self.username,
            password=self.password,
            application_name=f'{calling_function}()',
        )

        self.connection.autocommit = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def _check_connection_exists(self):
        if self.connection is None or self.connection.closed:
            raise RuntimeError('Connection not made yet.')

    def _execute_or_fetch_query_on_db(self, query: sql.Composable, fetch: bool = False) -> Optional[list]:
        self._check_connection_exists()
        cursor = self.connection.cursor()  # type:ignore

        # print(f"Executing query: ({query.as_string(connection)})")
        cursor.execute(query)
        # print(f"Succesfully executed query: ({cursor.query.decode()})")

        if fetch:
            records = cursor.fetchall()
            # print('Fetched records')
        else:
            records = None

        cursor.close()

        return records

    def fetch_with_query_on_db(self, query: sql.Composable) -> list:
        return self._execute_or_fetch_query_on_db(query, fetch=True)  # type:ignore

    def execute_query_on_db(self, query: sql.Composable) -> list:
        return self._execute_or_fetch_query_on_db(query, fetch=False)  # type:ignore

    def check_if_table_exists(self, schema_name: str, table_name: str) -> bool:
        exists_query = sql.SQL(
            """select exists (
                        select from information_schema.tables
                        where  table_schema = {schema_name}
                        and    table_name   = {table_name}
            )"""
        ).format(
            schema_name=sql.Literal(schema_name),
            table_name=sql.Literal(table_name),
        )
        exists = self.fetch_with_query_on_db(exists_query)[0][0]
        return exists

    def create_table_if_not_exists(self, schema_name: str, table_name: str, table_columns: sql.SQL, connection: Optional[Any] = None):
        table_exists_query = sql.SQL('select exists( select * FROM pg_catalog.pg_tables WHERE tablename = {table_name} and schemaname = {schema_name})').format(
            table_name=sql.Literal(table_name), schema_name=sql.Literal(schema_name)
        )
        table_exists = self.fetch_with_query_on_db(table_exists_query)[0][0]

        if not table_exists:
            create_table_query = sql.SQL('create table if not exists {schema_name}.{table_name} ({table_columns})').format(
                schema_name=sql.Identifier(schema_name),
                table_name=sql.Identifier(table_name),
                table_columns=table_columns,
            )
            self.execute_query_on_db(create_table_query)

    def insert_df(self, df: pd.DataFrame, schema: str, table: str) -> None:
        self._check_connection_exists()
        cursor = self.connection.cursor()  # type:ignore

        n_columns = df.shape[1]
        insert_string_part = ','.join(['%s'] * n_columns)
        insert_query = f'INSERT INTO {schema}.{table} VALUES ({insert_string_part}) ON CONFLICT do nothing'

        cursor.executemany(insert_query, df.values.tolist())
        self.connection.commit()  # type:ignore

        print('Data inserted successfully.')
