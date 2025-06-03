import xml.etree.ElementTree as ET
import json
import pandas as pd
from collections import namedtuple

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