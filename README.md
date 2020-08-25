[![Build Status](https://travis-ci.org/owuordickson/data-crossing.svg?branch=master)](https://travis-ci.org/owuordickson/data-crossing)

# FuzzTX

A Python implementation of the **FuzzTX** (Fuzzy Temporal Crossing) algorithm. The algorithm applies a fuzzy triangular membership function to cross time-series data from different and/or unrelated sources based on the *date-time* attributes. 
Research paper was accepted as a conference paper at the 2020 ADBIS, TPDL & EDA joint conferences: Owuor D.O., Laurent A., Orero J.O. (2020) Exploiting IoT Data Crossings for Gradual Pattern Mining Through Parallel Processing. In: Bellatreche L. et al. (eds) ADBIS, TPDL and EDA 2020 Common Workshops and Doctoral Consortium. TPDL 2020, ADBIS 2020. Communications in Computer and Information Science, vol 1260. Springer, Cham. https://doi.org/10.1007/978-3-030-55814-7_9


## Requirements

You will be required to install the following python dependencies before using **FuzzTX** algorithm:

``` shell
                   install python (version => 3.6)

```

``` shell
                    $ pip3 install numpy python-dateutil scikit-fuzzy

```

## Usage

Use it a command line program with the local package:

``` shell
$python3 src/init_fuzztx_csv.py -a allowChar -f 'file1.csv,file2.csv,file3.csv'
```

where you specify the input parameters as follows:

* **files.csv** - [required] files in csv format separated by commas

* **allowChar** - [optional] allow characters ```default = 0```. If set to 1, the algorithm will cross all columns including those that have non-numeric values.

For example we executed the **FuzzTX** algorithm on sample data-sets

``` shell
$python3 src/init_fuzztx_csv.py -a 0 -f '../data/oreme/GPS.csv,../data/oreme/Omnidir.csv'
```

### Output

The output should be a generated csv file **(x_data.csv)**. For purposes of demonstration, we display the contents (as a nested array) below

``` python
[
    ['timestamp', 'id_site', 'v1', 'v2', 'id_site', 'Rx', 'Hmax', 'Thmax', 'H1/3', 'Th1/3', 'Hmoy', 'Tmoy', 'Cambrure', 'Nb_Vagues'], 
    ['2012-01-01 00:30:00', '8', '49', '67', '1', '100.0000000000', '1.4900000000', '5.1700000000', '0.8600000000', '4.5700000000', '0.5400000000', '3.8000000000', '5.7000000000', '315'], 
    ['2012-01-01 01:29:58', '8', '52', '67', '1', '100.0000000000', '1.9500000000', '5.6600000000', '1.1500000000', '4.8600000000', '0.7500000000', '4.2300000000', '6.1000000000', '282']
]

0.0747671127319336 seconds

```

## License
* MIT

## References
* Dickson Owuor, Anne Laurent, and Joseph Orero (2019). Mining Fuzzy-temporal Gradual Patterns. In the proceedings of the 2019 IEEE International Conference on Fuzzy Systems (FuzzIEEE). IEEE. doi:10.1109/FUZZ-IEEE.2019.8858883
