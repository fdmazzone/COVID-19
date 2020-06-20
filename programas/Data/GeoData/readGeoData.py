#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:04:23 2020

@author: fernando
"""

import pandas as pd
import geopandas
import matplotlib.pyplot as plt

Arg=geopandas.read_file("departamento.json")
Arg[[h[:2]=='06' or h[:2]=='02' for h in Arg['in1']]].plot()