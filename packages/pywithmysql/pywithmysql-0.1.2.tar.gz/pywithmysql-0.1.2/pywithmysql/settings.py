from pywithmysql.config import DataBaseConfig
import pymysql.cursors


class SettingsTable:
    def __init__(self,
                 config: DataBaseConfig,
                 table_name: str
                 ) -> None:
        """
        Create class DataBaseConfig and insert to this class
        :param config: DataBaseConfig
        :param table_name: Your table name in your database
        """
        self.__config: dict = config.get_config
        self.__table_name: str = table_name

    def connect(self) -> None:
        """
        This method connected to your database with library pymysql
        getting data with your confign (host, port, user, password, database)
        :return: None
        """
        try:
            self.connection = pymysql.connect(
                host=self.__config["host"],
                port=self.__config["port"],
                user=self.__config["user"],
                password=self.__config["password"],
                database=self.__config["db_name"],
                cursorclass=pymysql.cursors.DictCursor
                )
            print("Connect successfully...\n")
        except Exception as ex:
            print(F"Connection error...\n{ex}")

    def create(self, names: list, values: list) -> None:
        """
        This method is insert data to your DB table
        :param names: list -> ["name", "password"]
        :param values: list -> ["'Alex'", "'7777'"]
        :return: None
        """
        with self.connection.cursor() as cursor:
            insert_query: str = F"""INSERT INTO `{self.__table_name}` ({",".join(names)}) VALUES
                                ({", ".join(values)});"""
            cursor.execute(insert_query)
            self.commit_transaction()
            print("Created...")

    def drop_table(self) -> None:
        audit_user: int = int(input(f"You are really want to drop table {self.__table_name}?\n1.Y/"
                                    f"\n2.N/"
                                    f"\nEnter>>> "))

        if audit_user == 1:
            with self.connection.cursor() as cursor:
                drop_table_query = F""" DROP TABLE IF EXISTS {self.__table_name}"""
                cursor.execute(drop_table_query)
                print("Table is drop")
                self.commit_transaction()

    def rename_column(self, old_name: str, new_name: str):
        with self.connection.cursor() as cursor:
            rename_column_query = F"""ALTER TABLE {self.__table_name} RENAME COLUMN {old_name} TO {new_name}"""
            cursor.execute(rename_column_query)
            print("Successfully rename...")
            self.commit_transaction()

    def update_data(self, names: tuple, values: tuple, id: int) -> None:
        with self.connection.cursor() as cursor:
            for index_value, name in enumerate(names, start=0):
                update_data = F"""UPDATE `{self.__table_name}` SET {name} = {values[index_value]} WHERE {self.__table_name}_id = {id} """
                cursor.execute(update_data)
                self.commit_transaction()

    def delete_for_id(self, id: int) -> None:
        with self.connection.cursor() as cursor:
            delete_user = F"""DELETE FROM `{self.__table_name}` WHERE {self.__table_name}_id = {id} """
            cursor.execute(delete_user)
            self.commit_transaction()

    def read_all(self) -> list[dict]:
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            select_all_data = F"""SELECT * from `{self.__table_name}`"""
            cursor.execute(select_all_data)

            rows = cursor.fetchall()
            return [item for item in rows]

    def read_for_column(self, column_parameter: str) -> list:
        result_rows: list = []
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            select_all_data = F"""SELECT * from `{self.__table_name}`"""
            cursor.execute(select_all_data)

            rows = cursor.fetchall()
            for row in rows:
                result_rows.append(row[column_parameter])

        return result_rows

    def read_with_filter(self, column_name: str, condition: str, value) -> list[dict]:
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = F"""SELECT * FROM `{self.__table_name}` WHERE {column_name} {condition} {value}"""
            cursor.execute(query)
            return [item for item in cursor.fetchall()]

    def begin_transaction(self) -> None:
        self.connection.begin()
        print("Transaction started...")

    def commit_transaction(self):
        self.connection.commit()
        print("Transaction committed...")

    def rollback_transaction(self) -> None:
        self.connection.rollback()
        print("Transaction rolled back...")

    def disconnect(self) -> None:
        self.connection.close()
        print("Disconnected...")