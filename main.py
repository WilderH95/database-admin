import pandas as pd
from dictionaries import teams, tri_codes, matches, team_db_ids
from data_handler import DataHandler
from db_admin import DBAdmin

COMPETITION = 193
DB_PATH = "C:/Users/Harry.Wilder/PycharmProjects/database-admin/data/PLP.mdb"

OPTA_F1 = 'data/F1_FixturesResults.xml'
SP_MATCH_LIST = 'data/Stats_Perform_Match_List.json'
# MATCH_IDS_CSV = 'PL_24.25_MATCH_IDs.csv'

# Initialise Opta Handler class (pass in latest F1 file from Opta)
data = DataHandler(OPTA_F1)

# Get all match dates and match times and put them into two lists
dates = data.get_match_dates()
times = data.get_match_times()

# Get all the home and away teams and put them into two lists
home_teams = data.get_home_teams()
away_teams = data.get_away_teams()

# Get all results and add to lists - work out the amount of results and fixtures outstanding
results = data.get_results()
home_team_scores = results.home_team_scores
away_team_scores = results.away_team_scores
amount_of_results = results.amount_of_results
amount_of_fixtures = results.amount_of_fixtures

# Use "teams" dictionary to translate opta ids into desired team names
home_teams_named = [teams[x] for x in home_teams]
away_teams_named = [teams[x] for x in away_teams]

# Get all Opta IDs and add them to a list
opta_ids = data.get_opta_ids()

# Get the venues and add them to a list
venues = data.get_venues()

# Use the "tri_codes" dictionary with the named home teams lists to create to separate social tag lists. Then call
# "create_social_tag" to join these into one list.
home_team_social = [tri_codes[x] for x in home_teams_named]
away_team_social = [tri_codes[x] for x in away_teams_named]
social_tags = data.create_social_tags(home_team_social, away_team_social)

# Use SS data to create a list of SS match IDs in the correct order. Note that the "social_tags" list must have been
# created with the "create_social_tags" method first, as the "social_tags" list is passed in to order the ids correctly.
sp_id_list = data.get_ss_ids(SP_MATCH_LIST, social_tags)

# Create a list of Team Talks matchweek ids. This will simply be a list of 10 identical digits from 1 to 38.
# Only call this and add it to the df/db when creating fixtures for first time.
tt_mws = data.create_tt_mws()

# Call the "create_match_ids" method to create a list of 380 match ids from 2500 onwards. Only call when creating a new
# db of matches.
match_ids = data.create_match_ids()

# Convert all team name strings into database id ints so that they can be entered as foreign keys into the db.
home_teams_db_id = [team_db_ids[x] for x in home_teams_named]
away_teams_db_id = [team_db_ids[x] for x in away_teams_named]

# Call the "create_fixs_dict" method and pass in all the above lists that have been created to populate the "matches" dict.
data.create_fixs_dict(COMPETITION, opta_ids, dates, times, home_teams_db_id, away_teams_db_id, venues,
                      social_tags, sp_id_list, tt_mws, amount_of_results, home_team_scores, away_team_scores,
                      amount_of_fixtures)

# Use pandas to translate the "matches" dictionary into a dataframe, then export this as a CSV using pandas.
pl_dataframe = data.create_df()

# pl_dataframe.to_csv("PL_Matches.csv")
# print("CSV created successfully.")

db_admin = DBAdmin(DB_PATH)

# USE BELOW CODE TO UPDATE DB WITH NEW MATCHES AT START OF SEASON
db_admin.populate_new_matches(pl_dataframe)
print("Database updated.")

# USE BELOW CODE TO UPDATE MATCHES WITH LATEST DATA THROUGHOUT SEASON
# db_admin.update_matches(pl_dataframe)
# print("Database updated.")