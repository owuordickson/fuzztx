# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"

"""

from datetime import datetime
from dateutil.parser import parse
import time
import numpy as np
import skfuzzy as fuzzy


class FuzzTXj:

    def __init__(self, json_data):
        if "datastreams" in json_data:
            self.observation_list, self.time_list = FuzzTXj.get_observations(json_data)
        else:
            raise Exception("Python Error: dataset has no observations")

    def cross_data(self):
        raw_data = self.observation_list
        time_data = self.time_list
        x_data = list()
        list_index = list()
        boundaries, extremes = self.get_boundaries()

        temp_tuple = list()
        temp_tuple.append("timestamp")
        for item in raw_data:
            var_title = item[0][1]
            temp_tuple.append(var_title)
        x_data.append(temp_tuple)

        while boundaries[1] <= extremes[1]:
            # while boundary is less than max_time
            arr_index = FuzzTXj.approx_fuzzy_index(time_data, boundaries)
            if arr_index:
                # print(arr_index)
                temp_tuple = FuzzTXj.fetch_x_tuples(boundaries[1], raw_data, arr_index, list_index)
                if temp_tuple:
                    x_data.append(temp_tuple)
                    list_index.append(arr_index)

            # do this until the raw_data is empty or it does not fit the mf
            # slide boundary
            new_bounds = [x+extremes[2] for x in boundaries]
            boundaries = new_bounds
        # print(list_index)
        return x_data

    def get_boundaries(self):
        min_time = 0
        max_time = 0
        max_diff = 0
        max_boundary = []
        # list_boundary = list()
        for item in self.time_list:
            temp_min, temp_max, min_diff = FuzzTXj.get_min_diff(item)
            # boundary = [(temp_min - min_diff), temp_min, (temp_min + min_diff)]
            # list_boundary.append(boundary)
            if (max_diff == 0) or (min_diff > max_diff):
                max_diff = min_diff
                max_boundary = [(temp_min - min_diff), temp_min, (temp_min + min_diff)]
            if (min_time == 0) or (temp_min < min_time):
                min_time = temp_min
            if (max_time == 0) or (temp_max > max_time):
                max_time = temp_max
        extremes = [min_time, max_time, max_diff]
        #return np.array(max_boundary), extremes
        return max_boundary, extremes

    @staticmethod
    def approx_fuzzy_index(all_pop, boundaries):
        list_index = list()
        for pop in all_pop:
            # for each boundary, find times with highest memberships for each dataset
            memberships = fuzzy.membership.trimf(np.array(pop), boundaries)
            if np.count_nonzero(memberships) > 0:
                index = memberships.argmax()
                list_index.append(index)
                # print(memberships)
            else:
                return False
        return list_index

    @staticmethod
    def fetch_x_tuples(time, data, arr_index, list_index):
        temp_tuple = list()
        # temp_tuple.append(time)
        temp_tuple.append(str(datetime.fromtimestamp(time)))
        for i in range(len(data)):
            index = (arr_index[i] + 1)
            # check if index already appears
            exists = FuzzTXj.check_index(i, arr_index[i], list_index)
            if exists:
                return False
            # print(exists)
            # pull their respective columns from raw_data to form a new x_data
            var_col = data[i][index][1]
            temp_tuple.append(var_col)
        return temp_tuple

    @staticmethod
    def check_index(i, value, arr_values):
        for item in arr_values:
            if item[i] == value:
                return True
        return False

    @staticmethod
    def get_min_diff(arr):
        arr_pop = np.array(arr)
        arr_diff = np.abs(np.diff(arr_pop))
        return arr_pop.min(), arr_pop.max(), arr_diff.min()

    @staticmethod
    def get_observations(json_data):
        list_observation = list()
        list_timestamps = list()
        for item in json_data["datastreams"]:
            temp_observations = list()
            temp_timestamps = list()
            title = ["timestamp", item["name"]]
            temp_observations.append(title)
            for obj in item["observations"]:
                ok, var_time = FuzzTXj.test_time(obj["time"])
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
