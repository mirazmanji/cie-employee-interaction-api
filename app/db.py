from db_config import DB_Config as conf
import mysql.connector

class Database:

    logging = None

    def __init__(self, logger):
        self.logging = logger

    def connect_db(self):
        self.logging.info('Database open connection request.')
        config = conf.config
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        self.logging.info('Database cursor created.')
        return cursor, connection

    def close_db(self, cursor, connection):
        self.logging.info('Database close connection request.')
        cursor.close()
        connection.close()
        self.logging.info('Database connection closed.')