# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 16:43:33 2015

@author: jivd78
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    elementos = []
    #get an iterable    
    context = ET.iterparse(filename, events = ('start','end'))
    #turn it into an iterator    
    context = iter(context)
    #get the root element:
    event, root = context.next()
    for event, element in context:
         elementos.append(element.tag)
    setico = set(elementos)
    for s in setico:
        i = 1
        for e in elementos:            
            if s == e:
                tags[s] = i
                i += 1
    for k in tags:
        if tags[k] != 1:
            tags[k]= tags[k]/2
    return tags
        


def test():
    #tags
    tags= count_tags(r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()
