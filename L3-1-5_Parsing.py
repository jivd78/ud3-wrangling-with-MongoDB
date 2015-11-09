# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 11:29:48 2015

@author: User
"""
'''
 To experiment with this code freely you will have to run this code locally.
 Take a look at the main() function for an example of how to use the code.
 We have provided example json output in the other code editor tabs for you to
 look at, but you will not be able to run any queries through our UI.
'''
import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    # This is the main function for making queries to the musicbrainz API.
    # A json document should be returned by the query.
    params["fmt"] = fmt
    #getting a response object named r
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    # This adds an artist name to the query parameters before making
    # an API call to the function above.
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    # After we get our output, we can format it to be more readable
    # by using this function.
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    '''
    Modify the function calls and indexing below to answer the questions on
    the next quiz. HINT: Note how the output we get from the site is a
    multi-level JSON document, so try making print statements to step through
    the structure one level at a time or copy the output to a separate output
    file.
    '''
    results = query_by_name(ARTIST_URL, query_type["aliases"], "Nirvana")
    pretty_print(results)
    #how many artist with similar names:
    Le = results['count']
    print 'artists key length: '+ str(Le)
    #appendig a list with all artist with similar names
    art_list = []
    for artist in results['artists']:
        art_list.append(artist['name'])
    
    #getting begin area for all groups:
#    begin_area = []
#    for artista in results['artists']:
#        for key in artista:
#            for key2 in key['begin-area']:
#                begin_area.append(key2['name'])

    #getting the first artist id in the list
    artist_id = results["artists"][1]["id"]
    print "\nARTIST:"
    pretty_print(results["artists"][1])
    
    #getting list first artist's data
    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    releases = artist_data["releases"]
    print "\nONE RELEASE:"
    release_titles = []
    disambiguations = []
    try:
        pretty_print(releases[0], indent=2)
        for r in releases:
            release_titles.append(r["disambiguation"])
        print "\nALL TITLES:"
        for t in release_titles:
            print t
    except IndexError as e:                
        print str(e) + ' : Can not find List index'
        
    return results, artist_id, artist_data, release_titles, art_list

results, artist_id,artist_data, release_titles, art_list = main()
if __name__ == '__main__':
    main()


