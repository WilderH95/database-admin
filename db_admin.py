import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine, text
from sqlalchemy.dialects import registry

registry.load("access.pyodbc")

DB_PATH = "C:/Users/Harry.Wilder/PycharmProjects/database-admin/data/PLP.mdb"

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
                CompID INT,
                OptaID INT,
                MatchDate DATETIME,
                KickOffTime TEXT(255),
                TeamID1 INT,
                TeamID2 INT,
                Score1 INT,
                Score2 INT,
                VenueID INT,
                Attendance TEXT(255),
                MatchHashTag TEXT(255),
                StatsPerformMatchID TEXT(255),
                TeamTalksMatchWeek INT,
                NeutralVenue YESNO,
                GoalRushMatchOrder, TEXT(255)
            )
        ''')
        pyodbc_conn.commit()
        cursor.close()
        pyodbc_conn.close()

    def populate_new_matches(self, df):
        # Convert df column types to match MS Access db column data types.
       # df['MatchId'] = df['MatchId'].astype('Int64')
        df['CompID'] = df['CompID'].astype('Int64')
        df['OptaID'] = df['OptaID'].astype('Int64')
        df['MatchDate'] = pd.to_datetime(df['MatchDate'])
        df['KickOffTime'] = df['KickOffTime'].astype(str)
        df['TeamID1'] = df['TeamID1'].astype('Int64')
        df['TeamID2'] = df['TeamID2'].astype('Int64')
        df['Score1'] = df['Score1'].astype('Int64')
        df['Score2'] = df['Score2'].astype('Int64')
        df['VenueID'] = df['VenueID'].astype('Int64')
       # df['Attendance'] = df['Attendance'].astype('Int64')
        df['MatchHashTag'] = df['MatchHashTag'].astype(str)
        df['StatsPerformMatchID'] = df['StatsPerformMatchID'].astype(str)
        df['TeamTalksMatchWeek'] = df['TeamTalksMatchWeek'].astype('Int64')
       # df['NeutralVenue'] = df['NeutralVenue'].astype(bool)
       # df['GoalRushMatchOrder'] = df['GoalRushMatchOrder'].astype(str)

        # Add the df to the MS Access db using df.to_sql
        params = urllib.parse.quote_plus(self.odbc_conn_str)
        alchemy_conn_str = f"access+pyodbc:///?odbc_connect={params}"
        engine = create_engine(alchemy_conn_str)
        df.to_sql(name="Matches", con=engine, if_exists='append', index=False)

    # to_sql does not work for updating rows with new data. Therefore the following must be done via manual sql statements
    def update_matches(self, df):
        # Connect to the db
        params = urllib.parse.quote_plus(self.odbc_conn_str)
        engine = create_engine(f"access+pyodbc:///?odbc_connect={params}")

        #Loop through all rows in "matches" and update results accordingly
        with engine.begin() as conn:
            for _, row in df.iterrows():
                # Check if the OptaID already exists
                result = conn.execute(
                    text("SELECT COUNT(*) FROM Matches WHERE OptaID = :id"),
                    {"id": row["OptaID"]}
                ).scalar()
                # Insert new row if OptaID does not exist
                if result == 0:
                    conn.execute(
                        text("""
                            INSERT INTO Matches (CompID, OptaID, MatchDate, KickOffTime, TeamID1, TeamID2, Score1, Score2
                            VenueID, MatchHashTag, StatsPerformMatchID, TeamTalksMatchWeek)
                            VALUES (:CompID, :OptaID, :MatchDate, :KickOffTime, :TeamID1, :TeamID2, :Score1, :Score2,
                            :VenueID, :MatchHashTag, :StatsPerformMatchID, :TeamTalksMatchWeek)
                        """), row.to_dict()
                    )
                # Update the row with new info if OptaID does exist
                else:
                    conn.execute(
                        text("""
                            UPDATE Matches
                            SET MatchDate = :MatchDate,
                                KickOffTime = :KickOffTime,
                                Score1 = :Score1,
                                Score2 = :Score2
                            WHERE OptaID = :OptaID
                        """), row.to_dict()
                    )

    # def validation_snapshot(self, df, key_column):
    #     ids_to_check = df[key_column].tolist()
    #     # Snapshot the db
    #     query = f"SELECT * FROM Matches WHERE {key_column} IN ({','.join(['?'] * len(ids_to_check))})"
    #     with engine.connect() as conn:
    #         df_before = pd.read_sql_query(query, conn, params=ids_to_check)