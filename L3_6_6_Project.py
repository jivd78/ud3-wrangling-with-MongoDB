# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:51:36 2015

@author: jivd78
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import codecs
import json
from string import maketrans
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for hat element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the ode from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED -array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""
#HARD CODED LISTS AND DICTIONARIES WITH CONSTANT STRINGS:======================

FILE = r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\medellin_colombia.osm'
FILE1 = r'C:\Users\User\Google Drive\Startup\Data Analyst Nanodegree\3-Data Munging with MongoDB\Python Scripts\Data\sao-paulo_brazil.osm'
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", \
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd": "Road",
            #"Ave": "Avenue",
            #"Ave.": "Avenue",
            #"Av.": "Avenue",
            #"Av": "Avenue",
            "Ave": "Avenida",
            "Ave.": "Avenida",
            "Av.": "Avenida",
            "Av": "Avenida",
            "R":"Rua",
            "R.":"Rua",
            "r":"Rua",
            "r.":"Rua",
            "Pr":"Praça",
            "Pr.":"Praça",
            "L":"",
            "L.":"Largo",
            "Lg":"Largo",
            "Lg.":"Largo",
            "lg":"Largo",
            "lg.":"Largo",            
            }
keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
#==============================================================================                                                        
#Compiled RE strings to  ease usage:===========================================

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_BR_re = re.compile(r'([\w]*\.*)', re.IGNORECASE)
#inner_key_re = re.compile(r':\S+\.?$', re.IGNORECASE)
#==============================================================================
#helper Functions Block========================================================
def key_type(element, keys):
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
#//////////////////////////////////////////////////////////////////////////////
def audit_street_type(street_name):
    street_types = defaultdict()
    m = street_type_BR_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type] = street_name
    return street_types
#//////////////////////////////////////////////////////////////////////////////
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
#//////////////////////////////////////////////////////////////////////////////
def is_address_key(elem):
    re_colon_sep = re.compile(':', re.IGNORECASE)   
    divided = re.split(re_colon_sep,elem, 1)
    if divided[0] == 'addr':
        return divided[1]
    else:
        return None
#//////////////////////////////////////////////////////////////////////////////        
def audit(osmtag):
    street_types = defaultdict(set)
    #if osmelement.tag == "node" or osmelement.tag == "way":
    #    for tag in osmelement.iter("tag"):
    if is_street_name(osmtag):
        street_types = audit_street_type(osmtag.attrib['v'])
    return street_types
#//////////////////////////////////////////////////////////////////////////////
def update_name(name, mapping):
    m = street_type_BR_re.search(name)
    current_street_type = m.group()
    try:
        name = re.sub(r'([\w]*\.*)',mapping[current_street_type],name, re.IGNORECASE)
    except KeyError:
        return name
    return name
#//////////////////////////////////////////////////////////////////////////////
def post_code_treatment(postcode_value):
    """
    This function substitues non alphanumeric characters ("."," " and "-" ) by no 
    character at all. Postcodes are transformed into numeric strings only.
    """
    pv = postcode_value
    translated_str = pv.replace("-","")
    translated_str = translated_str.replace(".","")
    translated_str = translated_str.replace(" ","")    
    return translated_str
    
#//////////////////////////////////////////////////////////////////////////////    
def non_tag_tags_treatment(element):
    #print element.tag
    if element.tag == "node" or element.tag == "way" :
        node = {}
        
        node['created'] = {x:str() for x in CREATED}
        # YOUR CODE HERE
        #Geting a tag's attribute dictionary with "attrib" method over ELEMENT 
        #class object.
        tag_attr = element.attrib
        #Since we know in advance dictionary keys, (gived in innicial comments),
        #we may use "if loops" to get and assign key values to the node dictionary.
        #key values are hard coded, but a more generalized implementation could 
        #be developed.
        node['type'] = element.tag        
        if tag_attr['id']:
            node['id'] = tag_attr['id']
        
        #We are appending first in "pos" list the latitude and then the longitude 
            #populating "created" inner dictionary:
            if tag_attr['changeset']:
                node['created']['changeset'] = tag_attr['changeset']
            if tag_attr['user']:
                node['created']['user'] = tag_attr['user']
            if tag_attr['version']:
                node['created']['version'] = tag_attr['version']
            if tag_attr['uid']:
                node['created']['uid'] = tag_attr['uid']
            if tag_attr['timestamp']:
                node['created']['timestamp'] = tag_attr['timestamp']
        #For way tags, lat and lon attributes don't exist, and sometimes visible 
        #attribute is missing also.
        try:
            if tag_attr['lat']:
                #initializing List elements inner dictionary.
                node['pos'] = []
                node['pos'].append(float(tag_attr['lat']))
        except KeyError as KE:
            node['pos'] = []
        try:
            if tag_attr['lon']:
                node['pos'].append(float(tag_attr['lon']))
        except KeyError as KE:
            if len(node['pos']) != 0:
                node['pos'].append(None)
            else:
                del node['pos']
        try:        
            if tag_attr['visible']:
                node['visible'] = tag_attr['visible']
        except KeyError as KE:
            node['visible'] = str()
        return node
    else:
        return None
#//////////////////////////////////////////////////////////////////////////////
def tag_tags_treatment(node, element):
    node['address'] = {}
    for tag in element.iter("tag"):
            tag_attrs = tag.attrib
            types = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
            k_classification = key_type(tag, types)
            #Now we proceed to procees every type according to instructions:
            for ky, va in k_classification.iteritems():
                if va != 0:
                    #checking for valid k tag values: Note that we test for lower
                    # and lower_colon values. Problemchars and other types are dissmissed
                    if ky == 'lower_colon':
                        #testing values for 'addr:street' only in k values, in 
                        #order to audit street name and transform it into a desire
                        #string format. If not street, also split it in colon and
                        #assign a value.
                        street_current_name = audit(tag)
                        if len(street_current_name) == 0:
                            #means that addr:street string was not found in k 
                            #attribute value, thus is a regular key.
                            #One more test for addr:XXX key type:
                            inner_key = is_address_key(tag_attrs['k'])
                            if inner_key != None:
                               #We test for postcode, then audit it 
                               #and transform it:
                                if inner_key == 'postcode':
                                    try:
                                        node['address']['postcode'] = \
                                            post_code_treatment(tag_attrs['v'])
                                    except UnicodeEncodeError:
                                        node['address']['postcode'] = tag_attrs['v']
                                        
                                else:
                                    node['address'][inner_key] = tag_attrs['v']
                            else: #Means inner_key is not an address key, so treat
                                  #it as any regular key:
                                string_splited = tag_attrs['k'].split(':')
                                node[string_splited[1]] = tag_attrs['v']
                                
                        else:
                            string_splited = tag_attrs['k'].split(':')
                            #We Map the expected or unexpected street types. If
                            #wrong, a helper function 'update_name is called to
                            #fix it. Mapping is a dictionary that maps wrong names
                            #into right names. This mapping is hard coded.
                            node['address'][string_splited[1]] = \
                                update_name(tag_attrs['v'], mapping)
                            #node['address'][string_splited[1]] = tag_attrs['v']
                    elif ky == 'lower':
                        node[tag_attrs['k']] = tag_attrs['v']
    return node
#//////////////////////////////////////////////////////////////////////////////
def nd_tags_treatment(node,element):
    if element.tag == "way" :
            node['node_refs'] = []
            for nd in element.iter('nd'):
                nd_attrs = nd.attrib
                node['node_refs'].append(nd_attrs['ref'])
    return node
#//////////////////////////////////////////////////////////////////////////////    
#End of Helper Functions ======================================================
#==============================================================================
#Core Functions Block:
def shape_element(element):
    """
    Shape_element function receives as argument a xml.etree.ElementTree.Element
    object, parses it only if the element's tag is a 'node' or a 'way' type tag. 
    Transforms a XML document content into a Dictionary structure document. 
    It is helpful when transforming XML documents into JSON documents.
    This function DOES NOT CREATE a JSON File, nor IMPORTS IT into MongoDB. 
    """
    node = non_tag_tags_treatment(element)
    if node != None:                
        #'tag' and 'way' tag types usually present child 'tag' tags, with 'k' 
        #and 'v' attributes. 'k' attribute values come in several types. We parse
        #this values and classify it in order to process it later.
        #key_types function make this classification:
        node = tag_tags_treatment(node,element)
        
        node = nd_tags_treatment(node,element)
        
        try:
            if len(node['address']) == 0:
                del node['address']
                return node
            else:
                return node
        except KeyError:
            return node
    else:
        return node

#In order to MongoDB import correctly the JSON file, pretty must be set False,
#otherwise, MongoDB will raise an error. 
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            print el
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

#End Core Functions Block======================================================
#==============================================================================
#testing function:
def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map(FILE1, False)
    pprint.pprint(data)
#    
#    correct_first_elem = {
#        "id": "261114295", 
#        "visible": "true", 
#        "type": "node", 
#        "pos": [41.9730791, -87.6866303], 
#        "created": {
#            "changeset": "11129782", 
#            "user": "bbmiller", 
#            "version": "7", 
#            "uid": "451048", 
#            "timestamp": "2012-03-28T18:31:23Z"
#        }
#    }
#    assert data[0] == correct_first_elem
#    assert data[-1]["address"] == {
#                                    "street": "West Lexington St.", 
#                                    "housenumber": "1412"
#                                      }
#    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
#                                    "2199822370", "2199822284", "2199822281"]



if __name__ == "__main__":
    test()    
