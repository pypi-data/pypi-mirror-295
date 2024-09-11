import pymysql


class DataBaseConfig:
    def __init__(self,
                 host: str,
                 port: int,
                 password: str,
                 user: str,
                 db_name: str
                 ) -> None:
        """
        Get data to connect
        :param host: str (Is your host database)
        :param port: int (Is your port database)
        :param password: str (Is your password database)
        :param user: str (Is you username database)
        :param db_name: str (Name database)
        """
        self.__host = host
        self.__port = port
        self.__password = password
        self.__user = user
        self.__db_name = db_name

    @property
    def get_config(self) -> dict:
        return {
            "host": self.__host,
            "port": self.__port,
            "user": self.__user,
            "password": self.__password,
            "db_name": self.__db_name
        }

