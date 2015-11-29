# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 19:59:21 2015

@author: jivd78
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should check the "k"
value for each "<tag>" and see if they can be valid keys in MongoDB, as well as
see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""

#r': raw string. interprets special characters as themselves.
#^:(caret).Matches the start of the string.and in MULTILINE mode also matches 
#  immediately after each newline.
#(...):Matches whatever regular expression is inside the parentheses, and 
#      indicates the start and end of a group; the contents of a group can be 
#      retrieved after a match has been performed, and can be matched later in 
#      the string with the \number special sequence, described below. To match 
#      the literals '(' or ')', use \( or \), or enclose them inside a character
#      class: [(] [)].
#[a-z]:Ranges of characters can be indicated by giving two characters and separating
#      them by a '-', for example [a-z] will match any lowercase ASCII letter,
#     [0-5][0-9] will match all the two-digits numbers from 00 to 59, and [0-9A-Fa-f]
#     will match any hexadecimal digit. If - is escaped (e.g. [a\-z]) or if it’s
#     placed as the first or last character (e.g. [a-]), it will match a literal '-'.
#|:   A|B, where A and B can be arbitrary REs, creates a regular expression that 
#     will match either A or B. An arbitrary number of REs can be separated by 
#     the '|' in this way. This can be used inside groups (see below) as well. 
#     As the target string is scanned, REs separated by '|' are tried from left
#     to right. When one pattern completely matches, that branch is accepted. 
#     This means that once A matches, B will not be tested further, even if it 
#     would produce a longer overall match. In other words, the '|' operator is
#     never greedy. To match a literal '|', use \|, or enclose it inside a character
#     class, as in [|].
#*: Causes the resulting RE to match 0 or more repetitions of the preceding RE,
#   as many repetitions as are possible. ab* will match ‘a’, ‘ab’, or ‘a’ followed
#   by any number of ‘b’s.
#$: Matches the end of the string or just before the newline at the end of the 
#   string, and in MULTILINE mode also matches before a newline. foo matches both
#  ‘foo’ and ‘foobar’, while the regular expression foo$ matches only ‘foo’. 
#   More interestingly, searching for foo.$ in 'foo1\nfoo2\n' matches ‘foo2’ 
#   normally, but ‘foo1’ in MULTILINE mode; searching for a single $ in 'foo\n' 
#   will find two (empty) matches: one just before the newline, and one at the 
#   end of the string.
#:  
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    # YOUR CODE HERE  
    atributos = element.attrib
    tag = element.tag
    if tag == 'tag':
        if re.search(lower,atributos['k']):
            keys["lower"] = keys["lower"] + 1
            
        elif re.search(lower_colon,atributos['k']):
            keys["lower_colon"] = keys["lower_colon"] + 1
            
        elif re.search(problemchars,atributos['k']):
            keys["problemchars"] = keys["problemchars"] + 1
        
        else:
            keys["other"] = keys["other"] + 1
            
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map(r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()
