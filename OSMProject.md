## OPEN STREET MAP PROJECT - DATA WRANGLING WITH MongoDB
###Jose Ignacio Valencia Diaz

Map Area: Sao Paulo - SP, Brazil.

https://www.openstreetmap.org/relation/298285

https://mapzen.com/data/metro-extracts . Once there look for Sao Paulo, Brazil

Although I was born in Colombia, I am currently living in Sao Paulo, Brazil. Sao Paulo is one of the most populous Megacities in the world, thus I decided to analyse its data on OMS and verify that despite the fact is a huge citiy, its data is not that helpful to use on apps developments.

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
There are several tags that could display related information, sometimes repetitive. In Sao Paulo database tags like name and street are commonly the same. the name tags has been missused. With the query of additional exploration can be seen this data feature. 
This excerpt for name tags displays name as streets.
    
    {u'type': u'way', u'name': u'Rua Francisco Jos\xe9 da Silva'}
    {u'type': u'way', u'name': u'Rua Jos\xe9 da Silva Ribeiro'}
    {u'type': u'way', u'name': u'Rua Aureliano Guimar\xe3es'}
    {u'type': u'way', u'name': u'Rua Engenheiro Ant\xf4nio Jovino'}
    {u'type': u'way', u'name': u'Rua Cidade do Rio Pardo'}
    {u'type': u'way', u'name': u'Rua N\xe9lson Gama de Oliveira'}
    {u'type': u'way', u'name': u'Rua Arnaldo Olinto Bastos Filho'}
    {u'type': u'way', u'name': u'Rua Jos\xe9 Gon\xe7alves'}
    {u'type': u'way', u'name': u'Rua Jos\xe9 de Oliveira Coelho'}
    {u'type': u'way', u'name': u'Rua Francisco Pessoa'}

Web tag and URL tag are another exampple of repetitive information. Additionally, genre tag could be mixed with amenity tag.
###4. Additional Exploration
With this query is possible to analize the most insightful tags.
    
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

This query yield some of the next results:
For  Amenities: Fuel Stations are the most tagged:
    
    {u'count': 1883429, u'_id': None}
    {u'count': 1393, u'_id': u'fuel'}
    {u'count': 1048, u'_id': u'parking'}
    {u'count': 892, u'_id': u'restaurant'}
    {u'count': 808, u'_id': u'school'}
    {u'count': 737, u'_id': u'bank'}
    {u'count': 458, u'_id': u'place_of_worship'}
    {u'count': 326, u'_id': u'pharmacy'}
    {u'count': 317, u'_id': u'fast_food'}
    {u'count': 285, u'_id': u'hospital'}
For Shop tags we have:
    
    {u'count': 1888947, u'_id': None}
    {u'count': 697, u'_id': u'supermarket'}
    {u'count': 618, u'_id': u'yes'}
    {u'count': 356, u'_id': u'bakery'}
    {u'count': 208, u'_id': u'car'}
    {u'count': 172, u'_id': u'car_repair'}
    {u'count': 167, u'_id': u'clothes'}
    {u'count': 140, u'_id': u'convenience'}
    {u'count': 134, u'_id': u'mall'}
    {u'count': 104, u'_id': u'hardware'}
And for Cuisine type:

    {u'count': 160, u'_id': u'regional'}
    {u'count': 113, u'_id': u'burger'}
    {u'count': 90, u'_id': u'pizza'}
    {u'count': 55, u'_id': u'japanese'}
    {u'count': 26, u'_id': u'sandwich'}
    {u'count': 22, u'_id': u'italian'}
    {u'count': 20, u'_id': u'coffee_shop'}
    {u'count': 10, u'_id': u'steak_house'}
    {u'count': 9, u'_id': u'international'}

###5 Conclusion
There are lot of value in geographical and localization data, even more if this is gathered toghether with extra data about the points tagged.
Databases produced from this data could generate powerful insights and have economic potencial.
All this is possible only if this data is highly populated. In the case this db lack enough information, for sure, any insight could lead to wrong conclusions or strategies, since data is not a representative sample of the entire population.
Marketing Open Street Data capabilities for new geographical support apps would be part of the solution, offering as main feature its free platform.
