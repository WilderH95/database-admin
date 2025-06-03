import xml.etree.ElementTree as ET
import json
import pandas as pd

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