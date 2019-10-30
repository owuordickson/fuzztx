# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"
@modified: "30 October 2019"

Usage:
    $python fuzztx_csv.py -f file1.csv,file2.csv,file3.csv

Description:
    f -> file paths to csv files

"""
import sys
from optparse import OptionParser
from algorithms.tx_csv import FuzzTX


def init_algorithm(f_paths):
    try:
        obj = FuzzTX(f_paths)
        x_data = obj.cross_data()
        # FuzzTX.write_csv(x_data)
        print(obj.f_paths)
        # print(obj.data_streams)
        # print(obj.time_list)
        # print(x_data)
    except Exception as error:
        print(error)


# ------------------------- main method ---------------------------------------------


if __name__ == "__main__":
    if not sys.argv:
        filePaths = sys.argv[1]
    else:
        optparser = OptionParser()
        optparser.add_option('-f', '--inputFile',
                             dest='files',
                             help='path to file containing csv',
                             # default=None,
                             default='../data/puechabon/puechabon_rainfall.csv,'
                                     '../data/puechabon/puechabon_evapotranspiration.csv,'
                                     '../data/puechabon/puechabon_temperature.csv',
                             type='string')
        (options, args) = optparser.parse_args()

        if options.files is None:
            print("Usage: $python fuzztx_csv.py -f file1.csv,file2.csv,file3.csv ")
            sys.exit('System will exit')
        else:
            filePaths = options.files

    import time
    start = time.time()
    init_algorithm(filePaths)
    end = time.time()
    print("\n"+str(end-start)+" seconds")