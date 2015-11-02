from flask import render_template
from app import app
from flask import request
import pymysql as mdb
from algo import getSentiment
from run import callAndStore
from tables import mysqlTables
from createDB import connectAndCreate, buildSchema
from math import fabs
#db = mdb.connect(user="root", passwd=' ', host="localhost", db="news", charset='utf8')
db = mdb.connect(user="root", passwd=' ', host="localhost", charset='utf8')


@app.route('/')
def cities_input():
  return render_template("index.html")

@app.route('/output')
def sentiment_output(chartID = 'bar_id', chart_type = 'column', chart_height = 500):
  
  company = request.args.get('ID')
  cursor = db.cursor()


  ''' clear db if needed '''

  if company == "clear db":
     cursor.execute('DROP DATABASE IF EXISTS news')   
     cursor.fetchall()
     cursor.close()
     cursor = db.cursor()
     return render_template("input.html")



  ''' create and use DB if not created already '''

  cursor.execute('CREATE DATABASE IF NOT EXISTS news')
  cursor.execute("USE news")



  ''' Check if 'news' is in database, if not create database and schema'''

  if not cursor.execute("SHOW TABLES LIKE 'articles';"):
     buildSchema(mysqlTables, cur=cursor)
     cursor.fetchall()
     print "table 'articles' newly created in db"
     cursor.close()
     cursor = db.cursor()



  ''' Check if 'company' is in article table else call NYT API and store in DB'''

  if cursor.execute("SELECT * FROM articles WHERE `companyName` LIKE '%s';" % company):
     cursor.fetchall()
     print "%s is already stored in DB, fetching articles..." % company
  else:
     callAndStore(company, cur = cursor, con=db)




  ''' fetch articles and calculate sentiment per article'''
  cursor.close()
  cursor = db.cursor()
  cursor.execute("SELECT pubDate, body, url FROM articles WHERE companyName=%s;",(company))

  query_results = zip(*cursor.fetchall())
  if len(query_results) == 0:
        message = "No Articles Found"
        return render_template('Error.html', message=message)
  try:
     senti = getSentiment(query_results[1])
  except: 
     print "Error while fetching query"
     return render_template('Error.html', message="...something went wrong!")


  withNegs = [x if x>0 else -1 for x in senti[0]]
  probsAbs = [x*y[0] if x<0 else x*y[1] for x,y in zip(withNegs,senti[1])]
  probs = [(l-.5)*2 if l>0 else (l+.5)*2 for l in probsAbs]
  totSent = sum([fabs(x) for x in probs])
  posSent = sum([x for x in probs if x>0])
  cum = 100*posSent/totSent
  if len(probs) < 5:
    cum = 0

  sorted_by_date = sorted(zip(query_results[0],probs,query_results[2]), key=lambda tup: tup[0])
  dateStr = map(lambda date: date.strftime('%m/%d/%Y'), zip(*sorted_by_date)[0])
  data =[{"y":a,"url":str(b)} for a,b in zip(zip(*sorted_by_date)[1],zip(*sorted_by_date)[2])]
  chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, 
           "backgroundColor": "#BFAF80",
           "plotShadow": "True"}
  
  series =[{"name": 'New York Times', "data": data, "color":"#8C6954","borderColor":"#8C6954"}]
  #title = {"text": "Article Sentiments", "style": {"color": "#FFFFFF","fontSize":"20"}}#"fontWeight":"bold",
  title = {"text": "", "style": {"color": "#FFFFFF","fontSize":"20"}}#"fontWeight":"bold",
  xAxis = {"categories": dateStr, "lineWidth": "2", "gridLineColor":"#FFFFFF", "labels": {"style": {"color": "#FFFFFF","fontSize":"20"}}}#"fontWeight":"bold",
  yAxis = {"title": {"text": 'Sentiment', "gridLineColor":"#FFFFFF", "style": {"color": "#FFFFFF","fontSize":"20"}}, "gridLineWidth": "2",  "labels": {"style": {"color": "#FFFFFF","fontSize":"20"}},#"fontWeight":"bold",
           "max": "1",
           "min": "-1"}
  gif = ""
  if cum > .2:
    string = "Sentiment Score: %2.0f%%" % cum
    gif = "/static/img/tUp.gif"
  elif cum < -0.2 :
    string = "Sentiment Score: %2.0f%%" % cum
    gif = "/static/img/tDown.gif"
  else:
    string = ""
    gif = "/static/img/neutral.gif"

  return render_template('output.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, comp=company.upper(), cum="%2.0f" %cum, gif=gif, string=string)#, plotOptions=plotOptions)
  

  
