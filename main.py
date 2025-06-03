import xml.etree.ElementTree as ET
import json
import pandas as pd
from dictionaries import teams, tri_codes, matches

COMPETITION = "Premier League"

OPTA_F1 = 'F1_FixturesResults.xml'
SP_MATCH_LIST = 'Stats_Perform_Match_List.json'
# MATCH_IDS_CSV = 'PL_24.25_MATCH_IDs.csv'
# TT_CSV = 'TT_MW_DATA.csv'

tree = ET.parse(OPTA_F1)
root = tree.getroot()

#TODO 1 - GET ALL THE MATCH DATES AND MATCH TIMES AND PUT THEM IN TWO LISTS - DONE

date_and_time = []

for n in range(380):
    date = root[0][n][0][0].text
    date_and_time.append(date)

dates = [date[0:10] for date in date_and_time]
times = [time[-8:-3] for time in date_and_time]

# print(dates)
# print(times)

#TODO 3 - GET ALL THE HOME TEAMS AND PUT THEM IN A LIST - DONE

home_teams = []

for n in range(380):
    home_team = root[0][n].find('TeamData').attrib['TeamRef']
    home_teams.append(home_team)

#TODO 4 - GET ALL THE AWAY TEAMS AND PUT THEM IN A LIST - DONE

away_teams = []

for n in range(380):
    try:
        away_team = root[0][n][5].attrib['TeamRef']
    except IndexError:
        away_team = root[0][n][4].attrib['TeamRef']

    away_teams.append(away_team)

#TODO 12 - HANDLE RESULTS AS WELL AS FIXTURES - DONE

# home_team_scores = []
#
# for n in range(380):
#     try:
#         home_team_score = root[0][n].find('TeamData').attrib['Score']
#         home_team_scores.append(home_team_score)
#     except KeyError:
#         pass
#
# away_team_scores = []
#
# for n in range(380):
#     try:
#         try:
#             away_team_score = root[0][n][5].attrib['Score']
#         except IndexError:
#             away_team_score = root[0][n][4].attrib['Score']
#         away_team_scores.append(away_team_score)
#     except KeyError:
#         pass
#
# amount_of_results = len(home_team_scores)
# amount_of_fixtures = 380 - amount_of_results

#TODO 5 - TRANSLATE OPTA IDs INTO ACTUAL TEAM NAMES - DONE

home_teams_named = [teams[x] for x in home_teams]
away_teams_named = [teams[x] for x in away_teams]

#TODO 6 - GET ALL THE OPTA MATCH IDs AND ADD THEM TO A LIST - DONE

opta_ids = []

for n in range(380):
    opta_id = root[0][n].attrib['uID'].strip("g")
    opta_ids.append(opta_id)

#TODO 7 - GET ALL THE VENUES AND ADD THEM TO A LIST - DONE

venues = []

for n in range(380):
    venue = root[0][n].find("Stat").text
    venues.append(venue)

#TODO 8 - CREATE THE MATCH SOCIAL TAGS AND ADD THEM TO A LIST - DONE

home_team_social = [tri_codes[x] for x in home_teams_named]
away_team_social = [tri_codes[x] for x in away_teams_named]

social_tags = []

for n in range(380):
    social_tag = f"#{home_team_social[n]}{away_team_social[n]}"
    social_tags.append(social_tag)

#TODO 9 - FIND A WAY TO GET AND HANDLE THE STATS PERFORM MATCH IDs - DONE

with open(SP_MATCH_LIST,"r", encoding="utf8") as sp_data_file:
    sp_data = json.load(sp_data_file)

sp_ids = {}

for n in range(380):
    sp_ids[f'#{sp_data["match"][n]["matchInfo"]["contestant"][0]["code"]}{sp_data["match"][n]["matchInfo"]["contestant"]
    [1]["code"]}'] = sp_data["match"][n]["matchInfo"]['id']
    
sp_id_list = [sp_ids[x] for x in social_tags]

#TODO 10 - CREATE A LIST OF 10x MATCHWEEK IDs ETC. - DONE

tt_mws = []
y = 0
for n in range(38):
    y += 1
    for x in range(10):
        tt_mws.append(y)

# print(tt_mws)
# print(len(tt_mws))

# tt_data = pandas.read_csv(TT_CSV)
# tt_records = tt_data.to_dict('records')
#
# tt_dict = {}
#
# for n in range(380):
#     tt_mw = str(tt_records[n]['TeamTalksMatchWeek'])
#     opta_id = str(tt_records[n]['OptaID'])
#     tt_dict[opta_id] = tt_mw

# ordered_tt_mws = [tt_dict[x] for x in opta_ids]

#TODO 14 - ENSURE THE MATCH ID NEVER CHANGES FOR EACH FIXTURE ONCE SET AT START OF SEASON
#import a csv of just match ids and opta ids from db
#match_id_data = pandas.read_csv(MATCH_IDS_CSV)
#match_id_records = match_id_data.to_dict('records')
#create a dictionary with opta ids as keys and corresponding match ids as values
#match_id_dict = {}
#
# for n in range(380):
#     match_id = str(match_id_records[n]['MatchId'])
#     opta_id = str(match_id_records[n]['OptaID'])
#     match_id_dict[opta_id] = match_id
#
# #create a list of match ids that match the order of the opta_ids list - ensuring the order of match ids corresponds
# # correctly to the list of opta ids
#
# ordered_match_ids = [match_id_dict[x] for x in opta_ids]

#TODO 11 - CREATE A DICTIONARY WITH MULTIPLE VALUES FOR THE KEY OF EACH MATCH - DONE

for n in range(380):
    # matches['MatchId'].append(ordered_match_ids[n])
    matches['Competition'].append(COMPETITION)
    matches['OptaID'].append(opta_ids[n])
    matches['MatchDate'].append(dates[n])
    matches['KickOffTime'].append(times[n])
    matches['TeamID1'].append(home_teams_named[n])
    matches['TeamID2'].append(away_teams_named[n])
    matches['Venue'].append(venues[n])
    matches['MatchHashTag'].append(social_tags[n])
    matches['StatsPerformMatchID'].append(sp_id_list[n])
    matches['TeamTalksMatchWeek'].append(tt_mws[n])

# for n in range(amount_of_results):
#     matches['Score1'].append(home_team_scores[n])
#     matches['Score2'].append(away_team_scores[n])

#Ensure the array is full for the data frame by adding None results to the remaining fixtures
# for n in range(amount_of_fixtures):
#     matches['Score1'].append(None)
#     matches['Score2'].append(None)

#TODO 13 - SAVE THE MATCHES DICTIONARY INTO A .CSV FILE - DONE

pl_dataframe = pd.DataFrame(matches)
# print(pl_dataframe)
pl_dataframe.to_csv("PL_Matches.csv")
print("CSV created successfully.")

#TODO 15 - PUT ALL THE ABOVE INTO A CLASS