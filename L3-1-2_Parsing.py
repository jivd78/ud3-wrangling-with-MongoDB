# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 11:11:56 2015

@author: User
"""
"""
 Your task is to read the input DATAFILE line by line, and for the first 10 lines (not including the header)
 split each line on "," and then for each line, create a dictionary
 where the key is the header title of the field, and the value is the value of that field in the row.
 The function parse_file should return a list of dictionaries,
 each data line in the file being a single list entry.
 Field names and values should not contain extra whitespace, like spaces or newline characters.
 You can use the Python string method strip() to remove the extra whitespace.
 You have to parse only the first 10 data lines in this exercise,
 so the returned list should have 10 entries!
"""
DATADIR = ""
DATAFILE = r"C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\beatles-diskography.csv"


def parse_file(datafile):
    data = []
    with open(datafile, "r") as f:
        header = f.readline().split(',')
        i = 0
        for line in f:
            if i == 10:
                break
            fields = line.split(',')
            entry = {}
            #enumerate method returns a a enumerate object that contains a tuple (count,values)
            for n, value in enumerate(fields):
                #.strip() method get rid from white spaces at beggining and end of a str object.
                entry[header[n].strip()] = value.strip()
            
            data.append(entry)
            i += 1
            #print line
    return data


def test():
    # a simple test of your implemetation
    datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_file(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

    
test()

