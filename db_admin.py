from dictionaries import *
from data_handler import DataHandler
import pyodbc
from sqlalchemy import create_engine

DB_PATH = "D:\Python-Projects\database-admin\PLP.mdb"

class DBAdmin:

    def __init__(self):
        # Connect with the database
        self.access_db_file = DB_PATH
        self.odbc_conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            fr'DBQ={self.access_db_file};'
        )

    def create_new_matches(self):
        pyodbc_conn = pyodbc.connect(self.odbc_conn_str)
        cursor = pyodbc_conn.cursor()
        table_name = "Matches"
        cursor.execute(f'''
            CREATE TABLE {table_name} (
                MatchId INT,
                Competition TEXT(255),
                OptaID INT,
                MatchDate DATETIME,
                KickOffTime DATETIME,
                TeamID1 TEXT(255),
                TeamID2 TEXT(255),
                Score1 INT,
                Score2 INT,
                Venue TEXT(255),
                MatchHashTag TEXT(255),
                StatsPerformMatchID TEXT(255),
                TeamTalksMatchWeek INT
            )
        ''')
        pyodbc_conn.commit()
        cursor.close()
        pyodbc_conn.close()