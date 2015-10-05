
# coding: utf-8

import dbSettings
import pandas as pd
from newspaper import Article


#import MySQLdb as db

##database = dbSettings.dbConfig["local"]
#con = db.connect(**database)
#cur = con.cursor()


def connectAndCreate(dbName=None, cur=None):
    #cur.execute('DROP DATABASE IF EXISTS news')
    cur.execute('CREATE DATABASE IF NOT EXISTS %s' % dbName) 
    cur.execute('USE %s' % dbName) 
    rs = cur.fetchall()
    return

def buildSchema(tables = None, cur=None):

    for table,vals in tables.iteritems():
        pFix = ""
        for key, val in vals:
            pFix = pFix +"%s %s, " % (key, val)
        cmd = "CREATE TABLE IF NOT EXISTS %s (%s)" % (table, pFix[:-2])
        cur.execute(cmd)
    return


def extractArticleBody(url):
    a = Article(url)
    a.download()
    a.parse() 
    return a.text


def storeArticleInDB(company=None, jsonResults=None, table=None, keyTuple=None, extras=None, cur=None, con=None):
    for jsonResult in jsonResults:
        valsString = ''
        keyA = ()  
        keyB = ()
      
        for a,b in keyTuple:
            keyA = keyA+(a,)
            keyB = keyB+(b,) 
        vals = tuple(["%s" % jsonResult[x] for x in keyB])
        for val in vals:
            if valsString == '':
                valsString = valsString + "'%s'" % val
            else:
                valsString = valsString + ", '%s'" % val

        keysString = ', '.join(map(str, keyA))
        if extras:
            for extra in extras:
                if extra[0] != "body":
                    keysString += ', ' + extra[0]
                    valsString += ", '%s'" % extra[1]
        cur.execute("use news")
        cur.execute("INSERT INTO articles (%s) VALUES (%s);"  %(keysString,valsString))
        if extras:
            for extra in extras:
                if extra[0] == "body":
                    body = extractArticleBody(jsonResult["web_url"])
                    #if "NYTimes.com no longer supports Internet Explorer 9 or earlier. Please upgrade your browser." in body:
                    #    return
                    #print "Body:", body
                    #print "WC:", jsonResult["word_count"]
                    #print "URL: ", jsonResult["web_url"]
                    att = "%s" % body
                    my_query = "UPDATE `articles` SET `body` = %s WHERE `id` = last_insert_id();"
                    cur.execute(my_query, (att,)) 
        rs = cur.fetchall()
        con.commit()
    return


def fetchArticleInDB(cur=None):
    cur.execute("use news")
    cur.execute("SELECT * FROM articles")
    cur.fetchall()
    return pd.read_sql_query("SELECT * FROM articles", con)
    
    
def storeCompanyInDB(company=None, cur=None):
        cur.execute("INSERT INTO companies (name) VALUES ('%s')" % (company))
        rs = cur.fetchall()
        return


def closeConnection(con=None):
    con.commit()
    con.close()

