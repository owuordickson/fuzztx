# simple Python code for getting only one site from data

import sys
from optparse import OptionParser
from algorithms.tx_csv import FuzzTX


def fetch_site(path, site_id, name):
    try:
        new_data = list()
        raw_data = FuzzTX.read_csv(path)
        size = len(raw_data)

        title = []
        for i in range(size):
            line = raw_data[i]
            if i == 0:
                title = line
            else:
                line_id = line[1]
                if int(line_id) == site_id:
                    new_data.append(line)
        new_data.sort(key=lambda x: x[0])
        new_data.insert(0, title)
        file = (name + '_site' + str(site_id) + '.csv')
        FuzzTX.write_csv(new_data, file)
        # return new_data
    except Exception as error:
        print(error)


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='file',
                         help='path to file containing csv',
                         # default=None,
                         default='../data/oreme/GPS.csv',
                         type='string')
    optparser.add_option('-n', '--siteId',
                         dest='siteId',
                         help='Id of the site to extract',
                         default=1,
                         type='int')
    optparser.add_option('-d', '--dataSet',
                         dest='dataName',
                         help='name of the data set',
                         default='data',
                         type='string')
    (options, args) = optparser.parse_args()

    if options.file is None:
        print("Usage: $python3 make_data.py -f data/oreme/GPS.csv -n 8 -d GPS")
        sys.exit('System will exit')
    else:
        file_path = options.file
        s_id = options.siteId
        data_name = options.dataName
        fetch_site(file_path, s_id, data_name)
