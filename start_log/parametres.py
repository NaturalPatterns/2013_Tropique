#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Created on Fri May 25 15:17:12 2012

@author: BIOGENE
"""

# une liste des kinects donnant leur adresse, port, position (x; y; z) et azimuth. 
info_kinects = [
#		{'address':'10.42.0.10', 'port': 9998, 'x':300.0, 'y':1, 'z': 4.3, 'az':+1.2 ,'max':504},#0
#		{'address':'10.42.0.10', 'port': 9999, 'x':100.0, 'y':1, 'z': 4.3, 'az':0 ,'max':495},#1
#		{'address':'10.42.0.11', 'port': 9998, 'x':300.0, 'y':1, 'z': 4.3, 'az':0 ,'max':495},#2
#		{'address':'10.42.0.11', 'port': 9999, 'x':300.0, 'y':1, 'z': 4.3, 'az':-1.2 ,'max':497},#3
#		{'address':'10.42.0.12', 'port': 9998, 'x':500.0, 'y':1, 'z': 4.3, 'az':0 ,'max':501},#4
#		{'address':'10.42.0.12', 'port': 9999, 'x':500.0, 'y':1, 'z': 4.3, 'az':+1.2 ,'max':497},#5
#		{'address':'10.42.0.13', 'port': 9998, 'x':300.0, 'y':-1, 'z': 4.3, 'az':+1.2 ,'max':505},#6
#		{'address':'10.42.0.13', 'port': 9999, 'x':300.0, 'y':-1, 'z': 4.3, 'az':-1.2 ,'max':489},#7
#		{'address':'10.42.0.14', 'port': 9998, 'x':300.0, 'y':-1, 'z': 4.3, 'az':0 ,'max':497},#8
#  		{'address':'10.42.0.14', 'port': 9999, 'x':500.0, 'y':-1, 'z': 4.3, 'az':0 ,'max':505},#9
#		{'address':'10.42.0.15', 'port': 9998, 'x':100.0, 'y':-1, 'z': 4.3, 'az':0 ,'max':491},#10
#		{'address':'10.42.0.15', 'port': 9999, 'x':100.0, 'y':-1, 'z': 4.3, 'az':-1.2 ,'max':491},#11
		{'address':'127.0.0.1', 'port': 9998, 'x':300.0, 'y':1, 'z': 4.3, 'az':+1.2 ,'max':504},#0
		]
  
DEBUG  = False
  
