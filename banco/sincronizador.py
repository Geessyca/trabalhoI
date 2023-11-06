import sys
import time
import mysql.connector
import datetime
import logging
from dotenv import load_dotenv
import os

sys.path.append(r'..')
logging.basicConfig(filename='../logs/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TableSync:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '../bd.env')
        load_dotenv(dotenv_path)
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
        self.port1 = os.getenv("PORT1")
        self.port2 = os.getenv("PORT2")

    def connect_to_database(self, host, user, password, database, port):
        try:
            db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            cursor = db.cursor()
            return db, cursor
        except mysql.connector.Error as err:
            logging.error(f"Failed to connect to the database: {err}")
            return None, None

    def sync_tables(self, table_name):
        db1, cursor1 = self.connect_to_database(self.host, self.user, self.password, self.database, self.port1)
        db2, cursor2 = self.connect_to_database(self.host, self.user, self.password, self.database, self.port2)

        if db1 and db2:
            cursor1.execute(f"SELECT COUNT(*) FROM {table_name}")
            rows_count_1 = cursor1.fetchone()[0]

            cursor2.execute(f"SELECT COUNT(*) FROM {table_name}")
            rows_count_2 = cursor2.fetchone()[0]

            if rows_count_1 != rows_count_2:
                if rows_count_1 < rows_count_2:
                    cursor1.execute(f"DELETE FROM {table_name}")
                    cursor2.execute(f"SELECT * FROM {table_name}")
                    data_to_insert = cursor2.fetchall()

                    columns = ', '.join([column[0] for column in cursor2.description])
                    placeholders = ', '.join(['%s'] * len(cursor2.description))
                    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                    cursor1.executemany(insert_query, data_to_insert)
                    db1.commit()
                else:
                    cursor2.execute(f"DELETE FROM {table_name}")
                    cursor1.execute(f"SELECT * FROM {table_name}")
                    data_to_insert = cursor1.fetchall()

                    columns = ', '.join([column[0] for column in cursor1.description])
                    placeholders = ', '.join(['%s'] * len(cursor1.description))
                    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                    cursor2.executemany(insert_query, data_to_insert)
                    db2.commit()
                
                logging.info("Sync process complete for all tables.")

        if db1:
            db1.close()
        if db2:
            db2.close()

    def sync(self):
        while True:
            self.sync_tables('sensores')
            self.sync_tables('atuadores')
            self.sync_tables('configuracoes')
            self.sync_tables('autenticacao')
            time.sleep(30)
