# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 11:11:55 2015

@author: jivd78
"""
'''
 Your task is to read the input DATAFILE line by line, and for the first 10 lines (not including the header)
 split each line on "," and then for each line, create a dictionary
 where the key is the header title of the field, and the value is the value of that field in the row.
 The function parse_file should return a list of dictionaries,
 each data line in the file being a single list entry.
 Field names and values should not contain extra whitespace, like spaces or newline characters.
 You can use the Python string method strip() to remove the extra whitespace.
 You have to parse only the first 10 data lines in this exercise,
 so the returned list should have 10 entries!
'''
import os
import csv
DATADIR = ""
DATAFILE = r"C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\beatles-diskography.csv"


def parse_file(datafile):
    data = []
    header = []
    with open(datafile, "r") as f: #open creates a file type object named f in this case:
        csvreader = csv.reader(f, delimiter =',')        
        i = 0
        for line in csvreader:
            if i == 0:
                header = line
                i += 1
            else:
                while i<=10:
                    data.append({header[0]:line[0],
                           header[1]:line[1],
                           header[2]:line[2],
                           header[3]:line[3],
                           header[4]:line[4],
                           header[5]:line[5],
                           header[6]:line[6]})
                    i += 1
                    line = next(csvreader)
            #print line
    return data

data =  parse_file(DATAFILE)

print data[0]
print data[9]

def test():
    # a simple test of your implemetation
    datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_file(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

test()
