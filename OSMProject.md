## OPEN STREET MAP PROJECT - DATA WRANGLING WITH MongoDB
###Jose Ignacio Valencia Diaz

Map Area: Sao Paulo - SP, Brazil.

https://www.openstreetmap.org/relation/298285

https://mapzen.com/data/metro-extracts . Once there look for Sao Paulo, Brazil

###1. Problems Encountered in the Map.
####1.1. Lack of Information Empty Addresses
Sao Paulo Metropolitan Area is one of the so called Mega Cities around the world. With a estimated population over 20 million and considered the economic engine of Brazil, the 15702 addresses tags encountered are incompatible with its real magnitud.
Moreover, this addresses brings 1974 empty adresses all from way type documents, whic leave us with only 13728 addresses. These addresses are from the entire metro area, i.e. not only from Sao Paulo itself, but from the other surrounding cities. 
(Sao Paulo: 7516 addresses, Sao Bernardo: 1784, Outras Cidades: 1764, Without City: 2664).
The next query show us the lack of useful addresses.

    non_addresses_SP = SaoPaulo.aggregate([{"$match":{"address.street":{"$exists":0},
                                                      "postal_code":{"$exists":0},
                                                      "address.postcode":{"$exists":0},
                                                      "type":"node"}},
                                           {"$group":{"_id":"$type",
                                                      "count":{"$sum":1}}},
                                           {"$sort": {"count":-1}}])
And this one show us the metropolitan cities within the downloaded range diminishing even more our cleaned database:

    cities_adr_SP = SaoPaulo.aggregate([{"$match":{"address.city":{"$exists":1}}},
                                        {"$group":{"_id":"$address.city",
                                                   "count_city":{"$sum":1}}},
                                        {"$sort":{"count_city":-1}}])
####1.2 Non Consistent Postcodes
Another way to locate an establishment is with its postal code. This attribute is preferred over an address itself, since, in theory, its uniformity is better than other address atributes uniformity, like streets, etc. Unfortunately, Sao Paulo post codes are formed by 8 digits, separeted or not by a hifen at fifth digit. Since this digit is correct, but not always produced, we decided to clean all postcodes, only remaining numeric characters.

####1.3 Street References
Sao Paulo language is Portuguese and gramatically speaking the street type is place at the beggining of any string. RE where compiled to match and search possible cases of Portuguese Streets.
this function cleans up post code issues:

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

This query let us analyse the final result of postcode cleaned up:

    postcodes_SP = SaoPaulo.find({"address:postcode": {"$exists":1}},
                                                      {"_id":0, "address:postcode":1})
    for a in postcodes_SP:
      print "post codes: ", a   

###2. Data  Overview
####2.1 File Sizes:

sao-paulo_brazil.osm...........360 Mb

sao-paulo_brazil.osm.json....439 Mb

####2.1. Number of Documents:
    
    SP_Count = SaoPaulo.find().count()
    1892840
####2.2 Number of Way Types:
    
    SP_ways = SaoPaulo.find({"type":"way"}).count()
    228558

####2.3 Number of Node Types:

    SP_nodes = SaoPaulo.find({"type":"node"}).count()
    1663935

####2.4 Number of Unique Users:
    
    SP_uusers = len(SaoPaulo.distinct("created.user"))
    1603
####2.5 Top 10 Contributor Users:
    
    topSP = SaoPaulo.aggregate([{"$group":{"_id":"$created.user",
                                          "count": {"$sum":1}}},
                               {"$sort":{"count": -1}},
                               {"$limit": 10}])
    [{u'count': 223228, u'_id': u'cxs'}
     {u'count': 134219, u'_id': u'MCPicoli'}
     {u'count': 109540, u'_id': u'AjBelnuovo'}
     {u'count': 106089, u'_id': u'ygorre'}
     {u'count': 85779, u'_id': u'Rub21'}
     {u'count': 68323, u'_id': u'Roberto Costa'}
     {u'count': 66989, u'_id': u'josedeonesio'}
     {u'count': 63604, u'_id': u'tenentebirula'}
     {u'count': 57345, u'_id': u'chdr'}
     {u'count': 41401, u'_id': u'naoliv'}]
####2.5 Only One Contribution Contributors:

    oneSP = SaoPaulo.aggregate([{"$group":{"_id":"$created.user",
                                           "count": {"$sum":1}}},
                                {"$group":{"_id":"$count",
                                           "countcounts":{"$sum":1}}},
                                {"$sort":{"_id":1}},
                                {"$limit":1}])
    [{u'_id': 1, u'countcounts': 311}]

###3. Additional Ideas:
####3.1. How to improve input data Volume.
There is no point of analysing data if this is not enough to get minimum insights.
For instance in a city with at least a pair of million of stablishments, must exists a way to improve significant data input beyond way type data.
It is very relevantt that 50% of all documents were input by only 10 users. Furthermore, 311 out of 1603 users only input a single document, nothing more.
Since Data driven apps and web development have exploited ih the last few years, and geographical positionament is common data but at some cost. It is important to hightlight for developers to point to free sources of this GP APIs. Open Street Map is a FREE source of this kind of data. If GP apps prefer Open Street Maps over Google Maps, data size and relevance could lead to a free cost revolution in this context.

####3.2. Tag Similarities, Repetitive Information, Related Information
There are several tags that could display related information, sometimes repetitive. Finding tags with related information or Standardizing Tags Keys may mark the difference
