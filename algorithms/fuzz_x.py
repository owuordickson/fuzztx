# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"

"""
import json
from dateutil.parser import parse
import time


class FuzzX:

    def __init__(self, file_path):
        self.json_data = FuzzX.read_json(file_path)
        if "crossingList" in self.json_data:
            # true
            self.observation_list = self.get_observations()
            self.x_data = list()
        else:
            raise Exception("Python Error: dataset has no observations")

    def get_observations(self):
        observations = list()
        for item in self.json_data["crossingList"]:
            temp_list = list()
            title = ["time", item["name"]]
            temp_list.append(title)
            for obj in item["observations"]:
                var_temp = [obj["time"], obj["value"]]
                temp_list.append(var_temp)
            observations.append(temp_list)
        return observations

    def cross_data(self):
        x = self.observation_list
        return False

    @staticmethod
    def read_json(file):
        with open(file, 'r') as f:
            temp_data = json.load(f)
        return temp_data

    @staticmethod
    def test_time(date_str):
        # add all the possible formats
        try:
            if type(int(date_str)):
                return False, False
        except ValueError:
            try:
                if type(float(date_str)):
                    return False, False
            except ValueError:
                try:
                    date_time = parse(date_str)
                    t_stamp = time.mktime(date_time.timetuple())
                    return True, t_stamp
                except ValueError:
                    raise ValueError('no valid date-time format found')
