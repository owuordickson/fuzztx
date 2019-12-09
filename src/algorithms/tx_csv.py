# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"

"""
import csv
from datetime import datetime
import numpy as np
import skfuzzy as fuzzy
from algorithms.datastream.datastream import DataStream


class FuzzTX:
    # allow user to upload multiple csv files

    def __init__(self, allow_char, file_paths):
        if allow_char == 0:
            self.allow_char = False
        else:
            self.allow_char = True
        self.f_paths = FuzzTX.test_paths(file_paths)
        if len(self.f_paths) >= 2:
            try:
                self.d_streams = self.get_data_streams()
                self.size = self.get_size()
                # self.data_streams, self.time_list = self.get_observations()
                print("data streams fetched")
            except Exception as error:
                raise Exception("CSV Error: "+str(error))
        else:
            raise Exception("Python Error: less than 2 csv files picked")

    def get_size(self):
        size = len(self.d_streams)
        return size

    def get_data_streams(self):
        list_ds = list()
        size = len(self.f_paths)
        for i in range(size):
            path = self.f_paths[i]
            ds = DataStream(i, path, self.allow_char)
            list_ds.append(ds)
        return list_ds

    def cross_data(self):
        print("starting crossing")
        d_streams = self.d_streams
        x_data = list()
        # list_index = list()
        boundaries, extremes = self.get_boundaries()

        temp_tuple = list()
        # add x_data title tuple
        temp_tuple.append("timestamp")  # add title for approximated timestamp
        for ds in d_streams:
            titles = ds.titles
            allowed_cols = ds.allowed_cols
            size = len(titles)
            for i in range(size):
                if i in allowed_cols:
                    temp_tuple.append(titles[i])
        x_data.append(temp_tuple)

        # add x_data value tuples
        while boundaries[1] <= extremes[1]:
            # while boundary is less than max_time
            arr_index = self.approx_fuzzy_index(boundaries)
            if arr_index:
                # print(arr_index)
                temp_tuple = self.fetch_x_tuples(boundaries[1], arr_index)
                if temp_tuple:
                    # print(temp_tuple)
                    x_data.append(temp_tuple)
            # do this until the raw_data is empty or it does not fit the mf
            # slide boundary
            new_bounds = [x + extremes[2] for x in boundaries]
            boundaries = new_bounds
        print("Finished crossing")
        return x_data

    def get_boundaries(self):
        min_time = 0
        max_time = 0
        max_diff = 0
        max_boundary = []
        # list_boundary = list()
        # for item in self.time_list:
        for ds in self.d_streams:
            arr_stamps = ds.timestamps
            temp_min, temp_max, min_diff = FuzzTX.get_min_diff(arr_stamps)
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
        return np.array(max_boundary), extremes

    def approx_fuzzy_index(self, boundaries):
        tuple_indices = list()
        # for pop in all_pop:
        for ds in self.d_streams:
            pop = ds.timestamps
            # for each boundary, find times with highest memberships for each dataset
            memberships = fuzzy.membership.trimf(np.array(pop), boundaries)
            if np.count_nonzero(memberships) > 0:
                index = memberships.argmax()
                var_index = [ds.id, index]
                tuple_indices.append(var_index)
                # tuple_indices.append(index)
                # print(memberships)
            else:
                return False
        return tuple_indices

    def fetch_x_tuples(self, time, arr_index):
        temp_tuple = list()
        temp_tuple.append(str(datetime.fromtimestamp(time)))
        all_ds = self.get_size()
        # for ds in self.d_streams:
        for j in range(all_ds):
            ds = self.d_streams[j]
            for item in arr_index:
                if (ds.id == item[0]) and (item[1] not in ds.fetched_tuples):
                    var_row = ds.data[item[1]]
                    self.d_streams[j].fetched_tuples.append(item[1])
                    size = len(var_row)
                    allowed_cols = ds.allowed_cols
                    for i in range(size):
                        if i in allowed_cols:
                            var_col = var_row[i]
                            temp_tuple.append(var_col)
                    break
        if len(temp_tuple) > 1:
            return temp_tuple
        else:
            return False

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
        no_zeros = np.argwhere(arr_diff)
        return arr_pop.min(), arr_pop.max(), no_zeros.min()

    @staticmethod
    def test_paths(path_str):
        path_list = [x.strip() for x in path_str.split(',')]
        for path in path_list:
            if path == '':
                path_list.remove(path)
        return path_list

    @staticmethod
    def write_csv(csv_data, path='x_data.csv'):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
            f.close()

    @staticmethod
    def write_file(data, path):
        with open(path, 'w') as f:
            f.write(data)
            f.close()
