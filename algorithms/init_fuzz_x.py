# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"

"""

from algorithms.fuzz_x import FuzzX


def init_algorithm():
    try:
        path = '../data/dataset.json'
        obj = FuzzX(path)
        print(obj.observation_list)
        print(obj.cross_data())
    except Exception as error:
        print(error)


init_algorithm()
