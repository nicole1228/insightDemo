
# coding: utf-8

import createDB as go
from tables import mysqlTables
from fetchNews import nytArticles, writeJson
import time


def callAndStore(companies=None, cur=None,con=None):
    #go.connectAndCreate(dbName='news', cur=cur)
    #go.buildSchema(mysqlTables, cur=cur)
    if companies is None:
        companies = ["Amazon","Microsoft","Google","Coca-Cola","Facebook"]
    articles = []
    for company in [companies]:
        for page in range(3):
        #if page % 2 == 0:
        #    continue
            time.sleep(.2)
            articles = nytArticles(qList=[company],headline=company, page=page, useBody=False)["response"]["docs"]
            go.storeArticleInDB(company, articles, table="articles", keyTuple= [("source","source"),("url","web_url"),("pubDate","pub_date")], extras=[("companyName",company),("body","body")], cur=cur, con=con)
