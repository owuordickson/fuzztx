# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "09 December 2019"

"""
import csv
from dateutil.parser import parse
import time


class DataStream:

    def __init__(self, _id, path, allow_char):
        self.id = _id
        self.path = path
        self.allow_char = allow_char
        self.raw_data = DataStream.read_csv(path)
        if len(self.raw_data) == 0:
            self.data = False
            print("csv file read error")
            raise Exception("Unable to read csv file: " + path)
        else:
            self.data = self.raw_data
            self.titles = self.get_titles()
            self.time_col = False
            self.allowed_cols, self.timestamps = self.init_ds()
            self.fetched_tuples = list()

    def get_titles(self):
        data = self.raw_data
        if data[0][0].replace('.', '', 1).isdigit() or data[0][0].isdigit():
            return False
        else:
            if data[0][1].replace('.', '', 1).isdigit() or data[0][1].isdigit():
                return False
            else:
                titles = []
                for i in range(len(data[0])):
                    # sub = [str(i+1), data[0][i]]
                    sub = str(data[0][i])
                    titles.append(sub)
                del self.data[0]
                return titles

    def init_ds(self):
        temp_timestamps = list()
        temp_allowed_cols = list()
        ds = self.data
        # test for time from any row
        t_index, stamp = DataStream.get_time_col(ds[1])
        if not stamp:
            raise Exception("No time found in file: " + str(self.path))
            # return False
        else:
            self.time_col = t_index
            for row in ds:
                size = len(row)
                for i in range(size):
                    cols, t_stamp = self.get_time_stamps(i, row)
                    temp_allowed_cols.append(cols)
                    temp_timestamps.append(t_stamp)
                    # return False
            # filter(lambda x: x != None, lis)
            temp_timestamps.sort()
            temp_allowed_cols.sort()
            print(temp_allowed_cols)
            print(temp_timestamps)
        return temp_allowed_cols, temp_timestamps

    def get_time_stamps(self, i, row):
        print("fetching time stamps")
        stamp = None
        index = None
        if self.time_col and i == self.time_col:
            # test for time
            t_value = row[i]
            try:
                time_ok, t_stamp = DataStream.test_time(t_value)
                if time_ok:
                    # temp_timestamps.append(t_stamp)
                    stamp = t_stamp
                else:
                    raise Exception(str(t_value) + ' : time is invalid for '
                                    + str(self.path))
            except ValueError:
                raise Exception(str(t_value) + ' : time is invalid for '
                                + str(self.path))
        else:
            # test for digits
            if self.allow_char:
                # temp_allowed_cols.append(i)
                index = i
            else:
                col_value = row[i]
                if col_value.replace('.', '', 1).isdigit() or col_value.isdigit():
                    # temp_allowed_cols.append(i)
                    index = i
        return index, stamp

    @staticmethod
    def get_time_col(row):
        size = len(row)
        for col_index in range(size):
            col_value = row[col_index]
            try:
                time_ok, t_stamp = DataStream.test_time(col_value)
                if time_ok:
                    return col_index, t_stamp
            except ValueError:
                continue
        return False, False

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
    def read_csv(file_path):
        # 1. retrieve data-set from file
        with open(file_path, 'r') as f:
            dialect = csv.Sniffer().sniff(f.readline(), delimiters=";,' '\t")
            f.seek(0)
            reader = csv.reader(f, dialect)
            temp = list(reader)
            f.close()
        return temp
