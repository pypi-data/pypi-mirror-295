import configparser
import os

import clickhouse_driver
import pandas
import psycopg
from clickhouse_driver import Client

from .errors.base import DatabaseNameError, FileExtensionError, ValidFileError

CLICKHOUSE = "clickhouse"
POSTGRESQL = "postgresql"
SUPPORTED_DATABASES = (CLICKHOUSE, POSTGRESQL)


class Database:
    def __init__(
        self,
        database_name: str,
        credentials_path: str,
        database_type: str = "clickhouse",
    ):
        """
        | Initialize the database class with the database name and location of the config.ini file.

        :param database_name: Name of the database name. Must be in the config.ini file
        :param credentials_path: Path to the config file
        :param database_type: Type of database to connect to
        """

        self._database_name = database_name
        self._credentials_path = credentials_path
        self._database_type = database_type
        self._validate_inputs()

        # load credentials
        dbconfig = configparser.ConfigParser(interpolation=None)
        dbconfig.read(credentials_path)
        if database_name in dbconfig.sections():
            self._host = dbconfig[database_name].get("host")
            self._user = dbconfig[database_name].get("user")
            self._password = dbconfig[database_name].get("password")
            self._port = dbconfig[database_name].get("port")
            self._db_name = dbconfig[database_name].get("db_name")

        else:
            raise DatabaseNameError(
                f"Database name {database_name} is not in the config file."
            )

    def _validate_inputs(self):
        """
        Validates the inputs provided to the Database class.
        """

        # check database type is supported
        if self._database_type not in SUPPORTED_DATABASES:
            raise ValueError(
                f"Database type '{self._database_type}' is not supported. Supported types are: "
                f"{', '.join(SUPPORTED_DATABASES)}."
            )

        # Check if ini file exists
        if not os.path.exists(self._credentials_path):
            raise ValidFileError("Please ensure the path to the config.ini is correct.")

        # check file ends with .ini
        _, file_extension = os.path.splitext(self._credentials_path)
        if file_extension.lower() != ".ini":
            raise FileExtensionError("Please ensure your config file ends with .ini.")

        # ensure the database type is included in the database name
        if self._database_type not in self._database_name:
            raise ValueError(
                "Please ensure the database type is part of the database name"
            )

    def connect_database(
        self, use_numpy: bool = False
    ) -> clickhouse_driver.Client | psycopg.Connection:
        """
        | Function to connect to the database

        :param: use_numpy: If numpy setting should be used for clickhouse connection
        :return: The Connection to the database
        """
        if self._database_type == "clickhouse":
            return Client(
                host=self._host,
                user=self._user,
                password=self._password,
                port = self._port,
                settings={"use_numpy": use_numpy},
            )
        elif self._database_type == "postgresql":
            return psycopg.connect(
                dbname=self._db_name,
                host=self._host,
                user=self._user,
                password=self._password,
                port=self._port,
            )

    def execute_query(self, query: str):
        """
        | Execute desired query on the database.

        :param query: Query to be executed
        """
        if self._database_type == "clickhouse":
            with self.connect_database() as db_con:
                db_con.execute(query)
        else:
            pg_con = self.connect_database()
            with pg_con.cursor() as cursor:
                cursor.execute(query)

    def read_from_database(self, query: str) -> pandas.DataFrame:
        """
        | Read from database using the provided query.

        :param query: Desired query to be executed and retrieved from database.
        :return: DataFrame containing the desired output
        """
        if self._database_type == "clickhouse":
            with self.connect_database() as db_con:
                return db_con.query_dataframe(query)
        else:
            pg_con = self.connect_database()
            with pg_con.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                return pandas.DataFrame(cursor.fetchall(), columns=columns)

    def save_to_database(
        self, data: pandas.DataFrame, table: str, schema: str, replace: bool = False
    ):
        """
        | Save desired DataFrame to the database.

        :param data: DataFrame to be saved
        :param table: Target table
        :param schema: Target schema
        :param replace: If True remove data and then add new data
        """

        if not isinstance(data, pandas.DataFrame):
            raise ValueError(
                f"Data type {type(data)} not supported, only pandas.DataFrame."
            )

        if self._database_type == "clickhouse":
            with self.connect_database(use_numpy=True) as db_con:
                if replace:
                    db_con.execute(f"TRUNCATE TABLE IF EXISTS {schema}.{table}")
                db_con.insert_dataframe(f"INSERT INTO {schema}.{table} VALUES", data)
        else:
            data = data.convert_dtypes()
            records = [
                tuple(y if not pandas.isna(y) else None for y in x)
                for x in data.to_numpy(dtype="object")
            ]
            columns = ",".join(list(data.columns))
            if not columns:  # nothing to push
                return
            pg_con = self.connect_database()
            cursor = pg_con.cursor()
            if replace:
                cursor.execute(
                    f"TRUNCATE {schema}.{table}"
                )  # delete content of the table
            with cursor.copy(f"COPY {schema}.{table} ({columns}) FROM STDIN") as copy:
                # superfast copy content to database
                for record in records:
                    copy.write_row(record)
