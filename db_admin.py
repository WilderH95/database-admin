import pandas as pd

from dictionaries import *
from data_handler import DataHandler
import pyodbc
from sqlalchemy import create_engine

DB_PATH = "PLP.mdb"

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

    def update_matches(self, df):
        # Convert df column types to match MS Access db column data types.
        df['MatchId'] = df['MatchId'].astype('Int64')
        df['CompID'] = df['CompID'].astype('Int64')
        df['OptaID'] = df['OptaID'].astype('Int64')
        df['MatchDate'] = pd.to_datetime(df['MatchDate'])
        df['KickOffTime'] = df['KickOffTime'].astype(str)
        df['TeamID1'] = df['TeamID1'].astype('Int64')
        df['TeamID2'] = df['TeamID2'].astype('Int64')
        df['Score1'] = df['Score1'].astype('Int64')
        df['Score2'] = df['Score2'].astype('Int64')
        df['VenueID'] = df['VenueID'].astype('Int64')
        df['Attendance'] = df['Attendance'].astype('Int64')
        df['MatchHashTag'] = df['MatchHashTag'].astype(str)
        df['StatsPerformMatchID'] = df['StatsPerformMatchID'].astype(str)
        df['TeamTalksMatchWeek'] = df['TeamTalksMatchWeek'].astype('Int64')
        df['NeutralVenue'] = df['NeutralVenue'].astype(bool)
        df['GoalRushMatchOrder'] = df['GoalRushMatchOrder'].astype(str)
        return df