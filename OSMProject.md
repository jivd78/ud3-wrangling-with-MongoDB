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

####1.2 Non Consistent Postcodes
Another way to locate an establishment is with its postal code. This attribute is preferred over an address itself, since, in theory, its uniformity is better than other address atributes uniformity, like streets, etc. Unfortunately, Sao Paulo post codes are formed by 8 digits, separeted or not by a hifen at fifth digit. Since this digit is correct, but not always produced, we decided to clean all postcodes, only remaining numeric characters.

####1.3 Street References
Sao Paulo language is Portuguese and gramatically speaking the street type is place at the beggining of any string. RE where compiled to match and search possible cases of Portuguese Streets.
this function cleans up post code issues:
'''

def post_code_treatment(postcode_value):
    pv = postcode_value
    translated_str = pv.replace("-","")
    translated_str = translated_str.replace(".","")
    translated_str = translated_str.replace(" ","")    
    return translated_str
'''










