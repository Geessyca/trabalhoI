import os
import sys
import threading
import time
import mysql.connector
import datetime
import logging
from dotenv import load_dotenv
logging.basicConfig(filename='D:/sd/trabalhoI/logs/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TableSync:
    def __init__(self, file_path):
        self.file_path = file_path
        dotenv_path = os.path.join(os.path.dirname(__file__), '../bd.env') 
        load_dotenv(dotenv_path)
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
        self.port1=os.getenv("PORT")
        if self.port1 == os.getenv("PORT1"):
            self.port2=os.getenv("PORT2")
        else:            
            self.port2=os.getenv("PORT1")

    def verificar_conexao(self, porta):
        try:
            cnx = mysql.connector.connect(
                host=self.host,
                port=porta,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cnx.close()
            return True
        except mysql.connector.Error as err:
            logging.error(f"Erro de conexão: {err}")
            return False

    def sincronizacao(self):
        port1 = self.verificar_conexao(self.port1)
        port2 = self.verificar_conexao(self.port2)

        if port1 and port2:
            self.sync_tables('sensores')
            self.sync_tables('atuadores')
            self.sync_tables('configuracoes')
            self.sync_tables('autenticacao')

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
                if rows_count_1 > rows_count_2:
                    cursor2.execute(f"DELETE FROM {table_name}")
                    cursor1.execute(f"SELECT * FROM {table_name}")
                    data_to_insert = cursor1.fetchall()
                    columns = ', '.join([column[0] for column in cursor1.description])
                    placeholders = ', '.join(['%s'] * len(cursor1.description))
                    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    cursor2.executemany(insert_query, data_to_insert)
                    db2.commit()
                logging.info("Sync process complete for all tables.")
                cursor1.close()
                cursor2.close()
                db1.close()
                db2.close()

    def sync(self):
        while True:
            dotenv_path = os.path.join(os.path.dirname(self.file_path), '../bd.env') 
            load_dotenv(dotenv_path)
            self.port1 = os.getenv("PORT")
            
            if self.port1 == os.getenv("PORT1"):
                self.port2 = os.getenv("PORT2")
            else:
                self.port2 = os.getenv("PORT1")
            
            self.sincronizacao()
            time.sleep(30)

if __name__ == "__main__":
    # Passe o caminho do arquivo ao instanciar a classe
    script_path = os.path.abspath(__file__)
    table_sync = TableSync(script_path)

    # Crie uma thread usando o método sync
    thread_sincron = threading.Thread(target=table_sync.sync)
    thread_sincron.start()