#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from glob import glob
import json

def json2WhenQ():
    """"""
    return None

def json2WhatQ():
    """"""
    return None

def json2HowMuchQ():
    """"""
    return None

def json2HowManyQ():
    """"""
    return None

def json2Where():
    """"""
    return None

if __name__ == "__main__":

#InputSTR
    inputLIST = []
    sourceDIR = "./dev_data"
    for f in glob("{}/*.json".format(sourceDIR)):
        inputLIST.append(json.load(open(f, mode="r", encoding="utf-8")))
    print(inputLIST)