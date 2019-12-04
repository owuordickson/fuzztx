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
from dateutil.parser import parse
from datetime import datetime
import time
import numpy as np
import skfuzzy as fuzzy


class FuzzTX:
    # allow user to upload multiple csv files

    def __init__(self, allow_char, file_paths):
        self.allow_char = allow_char
        self.f_paths = FuzzTX.test_paths(file_paths)
        if len(self.f_paths) >= 2:
            try:
                self.data_streams, self.time_list = self.get_observations()
            except Exception as error:
                raise Exception("CSV Error: "+str(error))
        else:
            raise Exception("Python Error: less than 2 csv files picked")

    def cross_data(self):
        raw_data = self.data_streams
        time_data = self.time_list
        digit_cols = list()
        x_data = list()
        list_index = list()
        boundaries, extremes = self.get_boundaries()

        j = 1
        temp_tuple = list()
        temp_tuple.append("timestamp")
        digit_cols.append(0)
        for item in raw_data:
            row_title = item[0]
            first_row = item[1]
            for i in range(1, len(row_title)):
                # ignore date-time column (already added above)
                col_name = row_title[i]
                var_col = first_row[i]

                try:
                    is_time, tstamp = FuzzTX.test_time(var_col)
                except ValueError as e:
                    is_time = False
                if not is_time:
                    temp_tuple.append(col_name)
                    if var_col.replace('.', '', 1).isdigit() or var_col.isdigit():
                        digit_cols.append(j)
                    j += 1
        new_tuple = list()
        for k in range(len(temp_tuple)):
            if self.allow_char == 0:
                if k in digit_cols:
                    new_tuple.append(temp_tuple[k])
            else:
                new_tuple.append(temp_tuple[k])
        x_data.append(new_tuple)
        # print(len(new_tuple))

        while boundaries[1] <= extremes[1]:
            # while boundary is less than max_time
            arr_index = FuzzTX.approx_fuzzy_index(time_data, boundaries)
            if arr_index:
                # print(arr_index)
                temp_tuple = self.fetch_x_tuples(boundaries[1], arr_index, list_index)
                if temp_tuple:
                    # print(temp_tuple)
                    new_tuple = list()
                    for k in range(len(temp_tuple)):
                        # if k not in time_cols:  # remove time cols
                        if self.allow_char == 0:
                            if k in digit_cols:
                                new_tuple.append(temp_tuple[k])
                        else:
                            new_tuple.append(temp_tuple[k])
                    x_data.append(new_tuple)
                    list_index.append(arr_index)
                    # print(len(new_tuple))
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
            temp_min, temp_max, min_diff = FuzzTX.get_min_diff(item)
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

    def get_observations(self):
        list_datasteam = FuzzTX.get_datastreams(self.f_paths)
        list_timestamps = list()
        for ds in list_datasteam:
            temp_timestamps = list()
            for i in range(1, len(ds)):
                # skip title row
                var_time = FuzzTX.get_time_col(ds[i])
                if not var_time:
                    return False, False
                temp_timestamps.append(var_time)
            list_timestamps.append(temp_timestamps)
        return list_datasteam, list_timestamps

    def fetch_x_tuples(self, time, arr_index, list_index):
        data = self.data_streams
        temp_tuple = list()
        temp_tuple.append(str(datetime.fromtimestamp(time)))
        for i in range(len(data)):
            index = (arr_index[i] + 1)
            # check if index already appears
            exists = FuzzTX.check_index(i, arr_index[i], list_index)
            if exists:
                return False
            # print(exists)
            # pull their respective columns from raw_data to form a new x_data
            # pull more than 1 column, test for time also
            # data[ds][row][col]
            var_row = data[i][index]
            for var_col in var_row:
                try:
                    is_time, tstamp = FuzzTX.test_time(var_col)
                except ValueError as e:
                    is_time = False
                if not is_time:
                    temp_tuple.append(var_col)
                    # if self.allow_char == 0:
                    #    if var_col.replace('.','',1).isdigit() or var_col.isdigit():
                    #        temp_tuple.append(var_col)
                        # else:
                        #    return False
                #    else:
                #        temp_tuple.append(var_col)
            # var_col = data[i][index][1]
            # temp_tuple.append(var_col)
        return temp_tuple

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
    def get_time_col(row):
        for col_value in row:
            try:
                time_ok, t_stamp = FuzzTX.test_time(col_value)
                if time_ok:
                    return t_stamp
            except ValueError:
                continue
        return False

    @staticmethod
    def get_datastreams(paths):
        list_observation = list()
        for path in paths:
            d_stream = FuzzTX.read_csv(path)
            if len(d_stream) > 1:
                list_observation.append(d_stream)
        if len(list_observation) >= 2:
            return list_observation
        else:
            raise Exception("Unable to read one or more CSV files")

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

    @staticmethod
    def test_paths(path_str):
        path_list = [x.strip() for x in path_str.split(',')]
        for path in path_list:
            if path == '':
                path_list.remove(path)
        return path_list

    @staticmethod
    def read_csv(file_path):
        # 1. retrieve data-set from file
        with open(file_path, 'r') as f:
            dialect = csv.Sniffer().sniff(f.readline(), delimiters=";,' '\t")
            f.seek(0)
            reader = csv.reader(f, dialect)
            temp = list(reader)
            f.close()
        return temp

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
