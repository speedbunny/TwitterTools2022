#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 05:36:13 2022

@author: saraheaglesfield
"""

import pandas as pd

df = pd.read_csv("followers.csv")
sample = df.sample(100)
