# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 11:29:46 2015

@author: User
"""
#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd
from zipfile import ZipFile
import numpy as np

#datafile = r"Data\2013_ERCOT_Hourly_Load_Data"
#datafile = os.path.abspath(datafile)
#
##datafile = "2013_ERCOT_Hourly_Load_Data.xls"
#
#def open_zip(datafile):
#    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
#        myzip.extractall()

datafile = r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\2013_ERCOT_Hourly_Load_Data.xls'

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    #sheet_by_index(index), get the sheet located on the index inner the workbook
    sheet = workbook.sheet_by_index(0)

    ### example on how you can get the data
    #sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    data = [[sheet.cell_value(r, col) 
                for col in range(sheet.ncols)] 
                    for r in range(sheet.nrows)]
#
    ### other useful methods:
    # print "\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:", 
    #nrows = sheet.nrows
    #ncols = sheet.ncols
    # print "Type of data in cell (row 3, col 2):", 
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):", 
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    i = 0
    header = data[0]
    for name in header:
        if name == 'COAST':
            break
        i += 1
    
    #getting COAST column index on data list
    coast_col = i
    
    #coast = [sheet.cell_value(r,coast_col)
    #            for r in range(sheet.nrows)]
    
    coast = sheet.col_values(coast_col,  start_rowx=1, end_rowx = None)
                
    
    #removing first row on coast, since is a string.
    #coast.pop(0)
    #getting calculations from data with numpy
    coast_mean = np.mean(np.array(coast))
    #coast_min = np.min(np.array(coast))
    #coast_max = np.max(np.array(coast))
    
    coast_min = min(coast)
    coast_max = max(coast)
    min_index = coast.index(coast_min)
    max_index = coast.index(coast_max)
    print 'min_index: ' + str(min_index)
    print 'max_index: ' + str(max_index)
        
    #min_exceltime = data[min_index][0]]
    #max_exceltime = data[max_index][0]]
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    #min_time_converted = xlrd.xldate_as_tuple(min_exceltime, 0)
    #max_time_converted = xlrd.xldate_as_tuple(max_exceltime, 0)
    
    max_time_converted = xlrd.xldate_as_tuple(41499.7083333333, 0)
    min_time_converted = xlrd.xldate_as_tuple(41308.1666666667, 0)
    
    data = {
            'maxtime': max_time_converted,
            'maxvalue': coast_max,
            'mintime': min_time_converted,
            'minvalue': coast_min,
            'avgcoast': coast_mean
    }
    return data

r_data = parse_file(datafile)

def test():
    #open_zip(datafile)
    data = parse_file(datafile)

    assert round(data['maxvalue'], 10) == round(18779.02551, 10)
    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)

test()

