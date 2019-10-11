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
            self.observation_list, self.time_list = FuzzX.get_observations(self.json_data)
            self.x_data = list()
        else:
            raise Exception("Python Error: dataset has no observations")

    def cross_data(self):
        x = self.observation_list
        return False

    @staticmethod
    def get_observations(json_data):
        list_observation = list()
        list_timestamps = list()
        for item in json_data["crossingList"]:
            temp_observations = list()
            temp_timestamps = list()
            title = ["timestamp", item["name"]]
            temp_observations.append(title)
            for obj in item["observations"]:
                ok, var_time = FuzzX.test_time(obj["time"])
                if not ok:
                    return False, False
                # var_temp = [obj["time"], obj["value"]]
                var_temp = [var_time, obj["value"]]
                temp_observations.append(var_temp)
                temp_timestamps.append(var_time)
            list_observation.append(temp_observations)
            list_timestamps.append(temp_timestamps)
        return list_observation, list_timestamps

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
                    raise ValueError('Python Error: no valid date-time format found')
