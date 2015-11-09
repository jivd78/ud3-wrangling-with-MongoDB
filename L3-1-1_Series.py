# -*- coding: utf-8 -*-

#!/usr/bin/env python
"""
Your task is to process the supplied file and use the csv module to extract data from it.
The data comes from NREL (National Renewable Energy Laboratory) website. Each file
contains information from one meteorological station, in particular - about amount of
solar and wind energy for each hour of day.

Note that the first line of the datafile is neither data entry, nor header. It is a line
describing the data source. You should extract the name of the station from it.

The data should be returned as a list of lists (not dictionaries).
You can use the csv modules "reader" method to get data in such format.
Another useful method is next() - to get the next line from the iterator.
You should only change the parse_file function.
"""
import csv
import os

DATADIR = "C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data"
DATAFILE = "745090.csv"

#datafile = os.path.abspath(datafile)


def parse_file(datafile):
    name = ""
    data = []
    with open(datafile,'r') as f_csv:
        csv_file = csv.reader(f_csv, delimiter = ',')
        i = 0
        for line in csv_file:            
            while i == 0:
                info = line
                name = str(info[1])
                i += 1
                next(csv_file)
            else:
                data.append(line)
                i += 1
    data.pop(0)
    
    #alternative code:

#    name = ""
#    data = []
#    with open(datafile,'rb') as f:
#        r = csv.reader(f)
#        name = r.next()[1]
#        header = r.next()
#        data = [row for row in r]

    # Do not change the line below
    return (name, data)


def test():
    datafile = r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\745090.csv'
    name, data = parse_file(datafile)

    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"
    
if __name__ == "__main__":
    test()
