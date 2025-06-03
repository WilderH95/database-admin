import xml.etree.ElementTree as ET
import json
from collections import namedtuple
from dictionaries import matches

class OptaHandler:

    def __init__(self, opta_f1):
        self.tree = ET.parse(opta_f1)
        self.root = self.tree.getroot()

    def get_match_dates(self):
        date_and_time = []

        for n in range(380):
            date = self.root[0][n][0][0].text
            date_and_time.append(date)

        dates = [date[0:10] for date in date_and_time]

        return dates

    def get_match_times(self):
        date_and_time = []

        for n in range(380):
            date = self.root[0][n][0][0].text
            date_and_time.append(date)

        times = [time[-8:-3] for time in date_and_time]

        return times

    def get_home_teams(self):
        home_teams = []

        for n in range(380):
            home_team = self.root[0][n].find('TeamData').attrib['TeamRef']
            home_teams.append(home_team)

        return home_teams

    def get_away_teams(self):
        away_teams = []

        for n in range(380):
            try:
                away_team = self.root[0][n][5].attrib['TeamRef']
            except IndexError:
                away_team = self.root[0][n][4].attrib['TeamRef']

            away_teams.append(away_team)

        return away_teams

    def get_results(self):
        Results = namedtuple('Results', ['home_team_scores','away_team_scores','amount_of_results',
                                         'amount_of_fixtures'])

        home_team_scores = []

        for n in range(380):
            try:
                home_team_score = self.root[0][n].find('TeamData').attrib['Score']
                home_team_scores.append(home_team_score)
            except KeyError:
                pass

        away_team_scores = []

        for n in range(380):
            try:
                try:
                    away_team_score = self.root[0][n][5].attrib['Score']
                except IndexError:
                    away_team_score = self.root[0][n][4].attrib['Score']
                away_team_scores.append(away_team_score)
            except KeyError:
                pass

        amount_of_results = len(home_team_scores)
        amount_of_fixtures = 380 - amount_of_results

        return Results(home_team_scores, away_team_scores, amount_of_results, amount_of_fixtures)

    def get_opta_ids(self):
        opta_ids = []

        for n in range(380):
            opta_id = self.root[0][n].attrib['uID'].strip("g")
            opta_ids.append(opta_id)

        return opta_ids

    def get_venues(self):
        venues = []

        for n in range(380):
            venue = self.root[0][n].find("Stat").text
            venues.append(venue)

        return venues

    def create_social_tags(self, home_team_social, away_team_social):
        social_tags = []

        for n in range(380):
            social_tag = f"#{home_team_social[n]}{away_team_social[n]}"
            social_tags.append(social_tag)

        return social_tags

    def get_ss_ids(self, sp_match_list, social_tags):
        with open(sp_match_list, "r", encoding="utf8") as sp_data_file:
            sp_data = json.load(sp_data_file)

        sp_ids = {}

        for n in range(380):
            sp_ids[
                f'#{sp_data["match"][n]["matchInfo"]["contestant"][0]["code"]}{sp_data["match"][n]["matchInfo"]["contestant"]
                [1]["code"]}'] = sp_data["match"][n]["matchInfo"]['id']

        sp_id_list = [sp_ids[x] for x in social_tags]

        return sp_id_list

    def create_tt_mws(self):
        tt_mws = []

        y = 0
        for n in range(38):
            y += 1
            for x in range(10):
                tt_mws.append(y)

        return tt_mws

    def create_match_ids(self):
        match_ids = []

        y = 2500
        for n in range(380):
            match_ids.append(y)
            y += 1

        return match_ids

    def create_fixs_dict(self, match_ids, competition, opta_ids, dates, times, home_teams_named, away_teams_named,
                         venues, social_tags, sp_id_list, tt_mws, amount_of_results, home_team_scores, away_team_scores,
                         amount_of_fixtures):
        for n in range(380):
            matches['MatchId'].append(match_ids[n])
            matches['Competition'].append(competition)
            matches['OptaID'].append(opta_ids[n])
            matches['MatchDate'].append(dates[n])
            matches['KickOffTime'].append(times[n])
            matches['TeamID1'].append(home_teams_named[n])
            matches['TeamID2'].append(away_teams_named[n])
            matches['Venue'].append(venues[n])
            matches['MatchHashTag'].append(social_tags[n])
            matches['StatsPerformMatchID'].append(sp_id_list[n])
            matches['TeamTalksMatchWeek'].append(tt_mws[n])

        for n in range(amount_of_results):
            matches['Score1'].append(home_team_scores[n])
            matches['Score2'].append(away_team_scores[n])

        # Ensure the array is full for the data frame by adding None results to the remaining fixtures
        for n in range(amount_of_fixtures):
            matches['Score1'].append(None)
            matches['Score2'].append(None)