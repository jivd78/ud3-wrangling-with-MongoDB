# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 12:51:26 2015

@author: jivd78
"""
import xml.etree.cElementTree as ET
from collections import defaultdict, OrderedDict
import pprint
import re
import codecs
import json
import L3_6_6_Project as P6
import pymongo as pm
#import keys
import pickle
import tarfile
from spyderlib.utils.iofuncs import load_dictionary

#Constants Block ==============================================================
FILE_M = r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\medellin_colombia.osm'
FILE_SP = r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\sao-paulo_brazil.osm'
md_key_path = r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\Med_tags.spydata'
sp_key_path = r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\SP_tags.spydata'

USAGE = ['landuse','amenity','speciality','especialidades','layer','usage', \
    'place','service','alt_name','name','reg_name','shop','social_facility', \
    'club','school','restaurant','cuisine','food','leisure']

WEB = ['url','website','wikipedia']

TRANSPORT = ['public_transport','rail','subway','monorail','busway','bus', \
    'trolleybus','trolley_wire', 'lines', 'route','station','cyclabilitY', \
    'bicycle','share_taxi','taxi']

GENRE = ['gender','genre','female','male','women','unisex']    

#importing key lists is they already exist.====================================

# a naive and incomplete demonstration on how to read a *.spydata file
# open a .spydata file
def load_spydata(filename):
    tar = tarfile.open(filename, "r")
    # extract all pickled files to the current working directory
    tar.extractall()
    extracted_files = tar.getnames()
    for f in extracted_files:
        if f.endswith('.pickle'):
            with open(f, 'rb') as fdesc:
                data = pickle.loads(fdesc.read())
    return data
# or use the spyder function directly:
#data_dict = load_dictionary(filename)


#Helper Function Block=========================================================
def find_keys(data):
    pattern = re.compile(r"'([\w]*)':", re.IGNORECASE)
 #   for line in data:
    print data
    lista = re.findall(pattern, str(data))
    return lista
#//////////////////////////////////////////////////////////////////////////////
def process_json(file_in):
    my_dic = []
    for _, element in ET.iterparse(file_in):
        el = P6.shape_element(element)
        if el:
            print 'dict fract: '
            print el
            my_dic.append(el)
    return my_dic
#//////////////////////////////////////////////////////////////////////////////    
def process_keys(file_in):
    key_list = []            
    for _, element in ET.iterparse(file_in):
        el = P6.shape_element(element)
        if el:
            line = find_keys(el)
            for l in line:
                key_list.append(l)
    s =set(key_list)
    s_list = []
    
    for ese in s:
        print ese
        s_list.append(ese)            
    return s_list
#==============================================================================
#Mongo queries block===========================================================
def get_client():
    client = pm.MongoClient('localhost', 27017)
    return client

#Testing Block ================================================================
def test(sp_key):
    """Receives a key path, load it and returns a dic with keys found in json 
       file"""
       
    SP_KeyD = load_spydata(sp_key)
    SP_Key = SP_KeyD['SP_tags']
    
    return SP_Key

def test1():
    #how many documents every collection has?:
    SP_Count = SaoPaulo.find().count()
    print "Number of documents: ", str(SP_Count)
    
    # how many ways and nodes:
    SP_ways = SaoPaulo.find({"type":"way"}).count()
    SP_nodes = SaoPaulo.find({"type":"node"}).count()
    print "Number of Way Types: ", str(SP_ways)
    print "Number of Node Types: ", str(SP_nodes)

    #how many unique users:
    SP_uusers = len(SaoPaulo.distinct("created.user"))
    print "Number of Unique Contributors: ", str(SP_uusers)

    #top10 contributer:
    topSP = SaoPaulo.aggregate([{"$group":{"_id":"$created.user",
                                          "count": {"$sum":1}}},
                               {"$sort":{"count": -1}},
                               {"$limit": 10}])    
    for tSP in topSP:
        print "Top Contributors Ranking: ", str(tSP)
    print ""    
    #Only One Contribution Contributors list:    
    oneSP = SaoPaulo.aggregate([{"$group":{"_id":"$created.user",
                                           "count": {"$sum":1}}},
                                {"$group":{"_id":"$count",
                                           "countcounts":{"$sum":1}}},
                                {"$sort":{"_id":1}},
                                {"$limit":1}])
    for oSP in oneSP:
        print "Number of One Contribution only Contributors: " + str(oSP)
                                    
    return SP_Count, SP_ways, SP_nodes, SP_uusers, topSP, oneSP

def test2(SP_Key):
    #Let's find how many tags of any kind has every collection
    tag_count_SP = {}
    
    for tag in SP_Key:
        tag_count_SP[tag] = SaoPaulo.find({str(tag): {"$exists":1}}).count()
        #print "tag: ", str(tag), "value: ", str(tag_count_SP[tag]) 
    
    #Tags most used. Sorted by value, not key
    Ord_tagSP= OrderedDict(sorted(tag_count_SP.items(), key=lambda t: t[1]))
    for k,v in Ord_tagSP.iteritems():
        print "key: ", str(k), "  Value: ", str(v)
    return Ord_tagSP

def querying():
    #Let's analyse address displaying:  
    #For Sao Paulo
    adr_SP = SaoPaulo.find({"address" : {"$exists":1}},
                  {"_id":0, "address":1})
    for a in adr_SP:
        print "Existing Addresses: ", str(a)
    print ""
    
    #All empty addresses are from way types. Nothing unexpected.
    empty_adr_SP = SaoPaulo.aggregate([{"$match":{"address.inclusion":{"$exists":1}}},
                                       {"$group":{"_id":"$type",
                                                  "count": {"$sum":1}}}])
    for a in empty_adr_SP:
        print "Empty Addresses: " + str(a)
    print ""
    
    #Adresses with Cities tags: 11064, SaoPaulo:7516 (68%), SaoBernardo:1784(16%)
    #Outras Cidades:1764 (16%)
    cities_adr_SP = SaoPaulo.aggregate([{"$match":{"address.city":{"$exists":1}}},
                                        {"$group":{"_id":"$address.city",
                                                   "count_city":{"$sum":1}}},
                                        {"$sort":{"count_city":-1}}])
    for a in cities_adr_SP:
        print "Cities within Range: " + str(a)
    print ""
    
    #Addresses without street, and/or post code: total nodes: 1663935. useless
    #addressnodes: 1654965. Useful Addresses: Only 8970 Useful Adresses.
    #Nodes with street only: 3294
    #Nodes with postal_code only: 0
    #Nodes with postcode only: 55
    #mixtured Street + postcode: 5620
    #mixtured street + postal_code: 1
    #mixtured street+postcode+postalcode: 0
    #USEFUL ADDRESSES: 3294+55+5620+1 = 8970
    non_addresses_SP = SaoPaulo.aggregate([{"$match":{"address.street":{"$exists":0},
                                                      "postal_code":{"$exists":0},
                                                      "address.postcode":{"$exists":0},
                                                      "type":"node"}},
                                           {"$group":{"_id":"$type",
                                                      "count":{"$sum":1}}},
                                           {"$sort": {"count":-1}}])
    for a in non_addresses_SP:
        print "Useless Addresses: " + str(a)
                                                                                
    #Let's analyse postcodes from SaoPaulo.
    postal_SP = SaoPaulo.aggregate([{"$match":{"address.postcode":{"$exists":1},
                                               "type":"node"}},
                                    {"$group":{"_id":"$type",
                                               "count":{"$sum":1}}},
                                    {"$sort": {"count":-1}}])
    for a in postal_SP:
        print "Postal Codes in Node Type: " + str(a)
        
    postcodes_SP = SaoPaulo.find({"address:postcode": {"$exists":1}},
                                 {"_id":0, "address:postcode":1})
    for a in postcodes_SP:
        print "post codes: ", a

def query1(Main_list, collection):
    #Usage block Tags:
    for tag in Main_list:
        cursor = collection.find({str(tag):{"$exists":1}},
                                 {"_id":0, "type":1, str(tag):1})
        for c in cursor:
            print c
        print " "
        parts = ['$', tag]
        string = ''.join(parts)
        cursor1 = collection.aggregate([{"$group":{"_id":string,
                                                   "count":{"$sum":1}}},
                                        {"$sort": {"count":-1}},
                                        {"$limit":10}])
        for c1 in cursor1:
            print c1
        print " "
#==============================================================================
if __name__ == "__main__":
    
    #Retrieving a dictionary list with JSONs
    Dic_List = process_json(FILE_SP)
    
    #Retrieving a list with unique tag k attributes.
    Key_list = process_keys(FILE_SP)    
    
    #getting a MongoDB client:
    client = get_client()
    
    #getting our databases:
    db = client.examples
    
    #getting a collection:
    SaoPaulo = db.SaoPauloV1
    
    #Getting all keys found in JSON file:    
    SP_keys_dict = test(sp_key_path)
    
    #Some basic queries:
    SP_Count, SP_ways, SP_nodes, SP_uusers, topSP, oneSP = test1()
    
    #Ordering Tags keys for Most used:
    Ord_tagSP  = test2(SP_keys_dict) 
    
    #Another queries:
    query1(USAGE, SaoPaulo)
    print """
    
    """
    query1(WEB, SaoPaulo)
    print """
    
    """
    query1(TRANSPORT, SaoPaulo)
    print """
    
    """
    query1(GENRE, SaoPaulo)
