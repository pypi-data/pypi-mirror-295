import pymysql.cursors
from pywithmysql.types import TypesEnum
from pywithmysql.config import DataBaseConfig
from pywithmysql.settings import SettingsTable
from typing import Any


class Column:
    def __init__(self,
                 name: str,
                 type_: TypesEnum,
                 nullable: bool = False,
                 max_length: int = 255,
                 default: Any = None,
                 unique: bool = False
                ) -> None:
        """
        Create column to your table
        :param name: str your Column name
        :param type_: import types (from pywithmysql.types import IntegerField, CharField, .......)
        :param nullable: bool
        :param max_length: int
        """
        self.__name = name
        self.__type = type_
        self.__nullable = nullable
        self.__max_length = max_length
        self.__default = default
        self.__unique = unique

    @property
    def get_all_data(self) -> dict:
        """
        Get all data from Column
        :return: dict (with data from Column)
        """
        return {
            "name": self.__name,
            "type": self.__type.__str__(self),
            "nullable": self.__nullable,
            "max_length": self.__max_length,
            "default": self.__default,
            "unique": self.__unique,
        }


class Table:
    def __init__(self,
                 table_name: str,
                 config: DataBaseConfig,
                 *columns: Column
                 ) -> None:
        """
        Connect to your DB with library pymysql
        :param table_name: str Your table_name in database
        :param metadata: DataBaseConfig your info
        :param columns: Column  (Column("name", Type, *args)
        """

        self.__table_name: str = table_name
        self.__config = config.get_config
        self.columns: tuple[Column] = columns

        self.connection = pymysql.connect(
            host=self.__config["host"],
            port=self.__config["port"],
            user=self.__config["user"],
            password=self.__config["password"],
            database=self.__config["db_name"],
            cursorclass=pymysql.cursors.DictCursor
        )

    def create_table(self) -> None:
        """
        Creating query to mysql with your data
        Library pymysql
        :return: None
        """
        with self.connection.cursor() as cursor:
            created_table_query: str = f""" CREATE TABLE `{self.__table_name}`(
                {self.__table_name}_id int AUTO_INCREMENT, """

            for index, column in enumerate(self.columns):
                column_data = column.get_all_data
                if column.get_all_data["type"] == "varchar":
                    created_table_query += f"""
                        {column_data["name"]} {column_data["type"]}
                        {f"({column_data['max_length']})"}
                        {"NOT NULL" if not column_data["nullable"] else "NULL"}
                        {f"DEFAULT '{column_data['default']}'" if column_data.get("default") is not None else ""}
                        {"UNIQUE" if column_data.get("unique") else ""}
                    """

                else:
                    created_table_query += f"""
                        {column_data["name"]} {column_data["type"]}
                        {"NOT NULL" if not column_data["nullable"] else "NULL"}
                        {f"DEFAULT '{column_data['default']}'" if column_data.get("default") is not None else ""}
                        {"UNIQUE" if column_data.get("unique") else ""}
                    """

                if index < len(self.columns) - 1:
                    created_table_query += ", "

            created_table_query += f", PRIMARY KEY ({self.__table_name}_id))"

            print("Created")
            cursor.execute(created_table_query)

    def __str__(self):
        return (F"Table `{self.__table_name}`:\n"
                F"Columns: {[F'Column {index}: {column.get_all_data}' for index, column in enumerate(self.columns, start=1)]}")


