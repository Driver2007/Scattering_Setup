#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:41:28 2017

@author: mellguth
"""

import time
import sys

i=0
while(True):
    print("Test output {idx}".format(idx=i))
    #sys.stdout.flush()
    i = i + 1
    time.sleep(1.0)
    
