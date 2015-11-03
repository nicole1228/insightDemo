
# coding: utf-8

import newspaper, json
from urllib2 import Request, urlopen, quote
import requests

def nytArticles(qList=["amazon"],headline='amazon', dates=("20131001","20151101"), page=1, useBody=True):
    news_desk = ["Business", "Education", "Energy", "Financial", "Politics", "Sunday Business","Business Day","None"]
    newsDString = " ".join(['"%s"' % x for x in news_desk])
    outFormat = "json"
    query = '?' 
    if useBody :
        query = '?q=%s&'% ('%22').join(qList)
    print "headline:", headline

#     qFilter = 'headline:%s&fq=source:("The New York Times")' % headline
    qFilter = 'headline:("%s")%%20AND%%20source:("The New York Times")%%20AND%%20news_desk:("%s")' % (headline.replace(" ","%20"), newsDString)
    #qFilter = 'headline:%s%%20AND%%20news_desk:("%s")' % (headline, newsDString)
    
    tup = dates+(page,)
    params = "begin_date=%s&end_date=%s&page=%s" % tup

    nytKey = "e5776a343b2afe42be49a27dea7f520d:11:72928865"
    request = "http://api.nytimes.com/svc/search/v2/articlesearch.%s%sfq=%s&%s&api-key=%s" % (outFormat, query, qFilter.replace(" ","%20"), params, nytKey)
    print "API Request: %s" % request 
    try:
        response = requests.get(request)
        #print "API Response: %s" % response.json()
        return response.json()

    except urllib2.URLError, e:
        print 'No articles, got an error code' , e


def writeJson(jsonOut):
    with open('result.json', 'w') as fp:
        json.dump(jsonOut, fp)




