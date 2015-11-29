# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 15:38:20 2015

@author: jivd78
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    users = set()
    user_list = []
    for _, element in ET.iterparse(filename):
        attributes = element.attrib
        if element.tag == 'node':
            user_list.append(attributes['uid'])
    users = set(user_list)
    for u in users:
        print u
    return users


def test():

    users = process_map(r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\example.osm')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()
