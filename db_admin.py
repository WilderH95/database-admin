import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine, text
from sqlalchemy.dialects import registry

registry.load("access.pyodbc")

class DBAdmin:

    def __init__(self, db_path):
        # Connect with the database
        self.db_path = db_path
        self.odbc_conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            fr'DBQ={self.db_path};'
        )
        params = urllib.parse.quote_plus(self.odbc_conn_str)
        self.engine = create_engine(f"access+pyodbc:///?odbc_connect={params}")

    def _convert_types(self, df):
        df = df.copy()
        df['CompID'] = df['CompID'].astype('Int64')
        df['OptaID'] = df['OptaID'].astype('Int64')
        df['MatchDate'] = pd.to_datetime(df['MatchDate'])
        df['KickOffTime'] = df['KickOffTime'].astype(str)
        df['TeamID1'] = df['TeamID1'].astype('Int64')
        df['TeamID2'] = df['TeamID2'].astype('Int64')
        df['Score1'] = df['Score1'].astype('Int64')
        df['Score2'] = df['Score2'].astype('Int64')
        df['VenueID'] = df['VenueID'].astype('Int64')
        df['MatchHashTag'] = df['MatchHashTag'].astype(str)
        df['StatsPerformMatchID'] = df['StatsPerformMatchID'].astype(str)
        df['TeamTalksMatchWeek'] = df['TeamTalksMatchWeek'].astype('Int64')
        return df

    def populate_new_matches(self, df):
        df = self._convert_types(df)
        df.to_sql(name="Matches", con=self.engine, if_exists='append', index=False)

    # to_sql does not work for updating rows with new data. Therefore the following must be done via manual sql statements
    def update_matches(self, df):
        df = self._convert_types(df)
        #Loop through all rows in "matches" and update results accordingly
        with self.engine.begin() as conn:
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