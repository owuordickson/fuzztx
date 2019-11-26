[![Build Status](https://travis-ci.org/owuordickson/data-crossing.svg?branch=master)](https://travis-ci.org/owuordickson/data-crossing)

# FuzzTX
A Python implementation of the <strong><em>FuzzTX</em></strong> algorithm. The algorithm applies a fuzzy triangular membership function to cross different unrelated data streams based on their <em>date-time</em> attributes. 
<!-- Research paper will appear in the proceedings of  -- link<br> -->

### Requirements:
You will be required to install the following python dependencies before using <em><strong>FuzzTX</strong></em> algorithm:<br>
```
                   install python (version => 3.6)

```

```
                    $ pip3 install numpy python-dateutil scikit-fuzzy

```

### Usage:
Use it a command line program with the local package:<br>
```
$python3 init_fuzztx_csv.py -a allowChar -f 'file1.csv,file2.csv,file3.csv'
```
where you specify the input parameters as follows:<br>
* <strong>files.csv</strong> - [required] files in csv format separated by commas<br>
* <strong>allowChar</strong> - [optional] allow characters ```default = 0``` <br>

For example we executed the <em><strong>ACO</strong>-GRAANK</em> algorithm with a sample data-set<br>
```
$python3 init_fuzztx_csv.py -a 0 -f '../data/oreme/GPS.csv,../data/oreme/Omnidir.csv'
```

<strong>Output</strong><br>
```
[
    ['timestamp', 'id_site', 'v1', 'v2', 'id_site', 'Rx', 'Hmax', 'Thmax', 'H1/3', 'Th1/3', 'Hmoy', 'Tmoy', 'Cambrure', 'Nb_Vagues'], 
    ['2012-01-01 00:30:00', '8', '49', '67', '1', '100.0000000000', '1.4900000000', '5.1700000000', '0.8600000000', '4.5700000000', '0.5400000000', '3.8000000000', '5.7000000000', '315'], 
    ['2012-01-01 01:29:58', '8', '52', '67', '1', '100.0000000000', '1.9500000000', '5.6600000000', '1.1500000000', '4.8600000000', '0.7500000000', '4.2300000000', '6.1000000000', '282']
]

0.0747671127319336 seconds

```

### License:
* MIT

### References
* Dickson Owuor, Anne Laurent, and Joseph Orero (2019). Mining Fuzzy-temporal Gradual Patterns. In the proceedings of the 2019 IEEE International Conference on Fuzzy Systems (FuzzIEEE). IEEE. doi:10.1109/FUZZ-IEEE.2019.8858883