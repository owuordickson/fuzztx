# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"
@modified: "09 December 2019"

Usage:
    $python3 init_fuzztx_csv.py -a 0 -f file1.csv,file2.csv,file3.csv -c 4

Description:
    f -> file paths to csv files

"""
import sys
from optparse import OptionParser
# from src import FuzzTX
from algorithms.tx_csv import FuzzTX


def init_algorithm(allow_char, f_paths, cores, allow_para):
    try:
        obj = FuzzTX(f_paths, allow_char, cores, allow_para)
        x_data = obj.cross_data()
        FuzzTX.write_csv(x_data)
        # print(x_data)

        if obj.allow_parallel:
            msg_para = "True"
        else:
            msg_para = "False"

        wr_line = "Algorithm: FuzzTX \n"
        wr_line += "No. of (crossed data) attributes: " + str(len(x_data[0])) + '\n'
        wr_line += "No. of (crossed data) tuples: " + str(len(x_data)) + '\n'
        wr_line += "Parallel multi-core execution: " + str(msg_para) + '\n'
        wr_line += ("Number of cores: " + str(obj.cores) + '\n\n')
        wr_line += ("\nFiles: " + f_paths + '\n')
        return wr_line
    except Exception as error:
        wr_line = "Failed: " + str(error)
        print(error)
        return wr_line


# ------------------------- main method ---------------------------------------------


if __name__ == "__main__":
    if not sys.argv:
        allowChar = sys.argv[1]
        filePaths = sys.argv[2]
        numCores = sys.argv[3]
    else:
        optparser = OptionParser()
        optparser.add_option('-a', '--allowChar',
                             dest='allowChar',
                             help='allow crossing of non-numeric columns',
                             default=0,
                             type='int')
        optparser.add_option('-f', '--inputFile',
                             dest='files',
                             help='path to file containing csv',
                             # default=None,
                             default='../data/oreme/GPS.csv,'
                                     # '../data/oreme/Directio.csv,'
                                     '../data/oreme/Omnidir.csv',
                             # default='../data/puechabon/puechabon_rainfall.csv,'
                             #        '../data/puechabon/puechabon_evapotranspiration.csv,'
                             #        '../data/puechabon/puechabon_global_radiation.csv,'
                             #        '../data/puechabon/puechabon_gross_primary_production_ecosystem_respiration.csv,'
                             #        '../data/puechabon/puechabon_net.csv,'
                             #        '../data/puechabon/puechabon_photosynthetic_active_radiation.csv,'
                             #        '../data/puechabon/puechabon_temperature.csv',
                             type='string')
        optparser.add_option('-c', '--coresCount',
                             dest='numCores',
                             help='number of cores',
                             default=1,
                             type='int')
        optparser.add_option('-p', '--allowParallel',
                             dest='allowPara',
                             help='allow parallel multiprocessing',
                             default=0,
                             type='int')
        (options, args) = optparser.parse_args()

        if options.files is None:
            print("Usage: $python3 init_fuzztx_csv.py -a 0 -f file1.csv,file2.csv,file3.csv -c 4")
            sys.exit('System will exit')
        else:
            filePaths = options.files
            allowChar = options.allowChar
            numCores = options.numCores
            allowPara = options.allowPara

    import time
    start = time.time()
    res_text = init_algorithm(allowChar, filePaths, numCores, allowPara)
    end = time.time()

    wr_text = ("Run-time: " + str(end - start) + " seconds\n")
    wr_text += str(res_text)
    f_name = ('res_x' + str(end).replace('.', '', 1) + '.txt')
    FuzzTX.write_file(wr_text, f_name)
    print(wr_text)
