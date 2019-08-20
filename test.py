# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 21:19:14 2019

@author: a179227
"""

from compression import decodbin, decbin


payl=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1]
long = 32
rang = 0
msg = decbin(payl, long, rang)
print(msg)