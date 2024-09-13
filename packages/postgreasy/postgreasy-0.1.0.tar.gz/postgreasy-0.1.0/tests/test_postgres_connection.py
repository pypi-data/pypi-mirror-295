import uuid
import pandas as pd
import pytest
from psycopg2 import sql

from src.postgreasy import PostgresConnection


def test_connect():
    with PostgresConnection() as conn:
        x = conn.fetch_with_query_on_db('select 1')
        print(x)
        assert x == [(1,)]


def test_disconnect():
    with PostgresConnection() as conn:
        x = conn.fetch_with_query_on_db('select 1')
        assert x == [(1,)]

    with pytest.raises(RuntimeError):
        conn.fetch_with_query_on_db('select 1')


def test_insert():
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [5, 28, 8]})
    test_table = f'test_insert_{str(uuid.uuid4())[:4]}'
    with PostgresConnection(database='ovviadatatransaction_test') as conn:
        conn.create_table_if_not_exists('public', test_table, sql.SQL('x int, y int'))
        conn.insert_df(df, 'public', test_table)
        records = conn.fetch_with_query_on_db(sql.SQL('select * from {test_table}').format(test_table=sql.Identifier(test_table)))
        conn.execute_query_on_db(sql.SQL('drop table {test_table}').format(test_table=sql.Identifier(test_table)))
        print(records)
        assert records == [(1, 5), (2, 28), (3, 8)]
