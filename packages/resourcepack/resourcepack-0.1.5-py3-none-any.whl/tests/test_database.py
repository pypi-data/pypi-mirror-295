import os

import pandas as pd
import pytest

from resourcepack.errors.base import ValidFileError

from resourcepack.database import Database, SUPPORTED_DATABASES

config_path = os.environ["CONFIG_PATH"]


@pytest.mark.database
class TestCleanOrganization:
    def test_database_init(self):
        # test the path to the credentials
        wrong_path = 'some/path'
        try:
            db = Database('clickhouse', wrong_path, 'clickhouse')
        except ValidFileError as e:
            assert str(e) == "Please ensure the path to the config.ini is correct."

        # check the database is one of the supported ones
        try:
            db = Database('clickhouse', config_path, 'wrong_db')
        except ValueError as e:
            assert str(e) == (f"Database type 'wrong_db' is not supported. Supported types are: "
                              f"{', '.join(SUPPORTED_DATABASES)}.")

        # check the database name is in the config file
        try:
            db = Database('wrong_db', config_path, 'clickhouse')
        except ValueError as e:
            assert str(e) == "Please ensure the database type is part of the database name"

        try:
            db = Database('postgres local', config_path, 'clickhouse')
        except ValueError as e:
            assert str(e) == "Please ensure the database type is part of the database name"

    def test_clickhouse_connection(self):
        # test connection to clickhouse instance
        db = Database('database clickhouse', config_path, 'clickhouse')
        try:
            with db.connect_database() as db_con:
                result = db_con.execute('SELECT version()')
            return f"Connection successful, ClickHouse server version: {result[0][0]}"
        except Exception as e:
            assert False, str(e)

    def test_clickhouse_read_and_save(self):
        db = Database('database clickhouse', config_path, 'clickhouse')
        try:
            df = pd.DataFrame(data=[[1, 2], [3, 4]], columns=['a', 'b'])
            db.execute_query("""
                   CREATE TABLE IF NOT EXISTS default.test
                   (
                        a int,
                        b int
                        )
                   ENGINE = MergeTree
                   ORDER BY a
                   SETTINGS storage_policy = 'default';
            """)
            db.save_to_database(df, table='test', schema='default', replace=True)
            df_new = db.read_from_database("SELECT * FROM default.test")
            db.execute_query("DROP TABLE IF EXISTS default.test")
            assert df.equals(df_new), "There is an error with the clickhouse connection"
        except Exception as e:
            assert False, str(e)
    #
    # def test_postgresql_connection(self):
    #     db = Database('postgresql new', config_path, 'postgresql')
    #     try:
    #         with db.connect_database() as db_con:
    #             db_con.execute('SELECT version()')
    #     except Exception as e:
    #         assert False, str(e)
    #     try:
    #         df = pd.DataFrame(data=[[1, 2], [3, 4]], columns=['a', 'b'])
    #         db.execute_query("""CREATE SCHEMA test""")
    #         db.execute_query("""
    #                            CREATE TABLE IF NOT EXISTS sometest.test
    #                            (
    #                                 a int,
    #                                 b int
    #                                 );
    #                     """)
    #     except Exception as e:
    #         return e
