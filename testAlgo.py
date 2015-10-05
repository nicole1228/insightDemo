import pandas as pd
import numpy as np
import os
import json
import pprint
import urllib
from cleanedDict2 import rows as dictRows
from nlpHelpers import Splitter, POSTagger, DictionaryTagger#, sentiment_score
from nltk.stem.wordnet import WordNetLemmatizer
from newspaper import Article
import math
from sklearn.ensemble import RandomForestClassifier


def setup():
    splitter = Splitter()
    postagger = POSTagger()
    df = pd.DataFrame(data = dictRows, columns=['word', 'pos', 'neg'])

    posPath = "testReviews/txt_sentoken/pos/"
    negPath = "testReviews/txt_sentoken/neg/"


    trainFiles = {"pos": {"files" : os.listdir(posPath)[:300],
                          "path" : posPath,
                          "y" : 1},
                  "neg": {"files" : os.listdir(negPath)[:300],
                          "path" : negPath,
                          "y" : 0}}

    testFiles = {"pos": {"files" : os.listdir(posPath)[200:400],
                         "path" : posPath,
                         "y" : 1},
                 #"neg": {"files" : os.listdir(negPath)[10:20],
                 #        "path" : negPath,
                 #        "y" : 0}

                 }
    return df, trainFiles, testFiles, splitter, postagger


clf = RandomForestClassifier()


def readFile(l):
    f = open("/".join(l), 'r')
    content = f.read()
    f.close()
    return content

def extractFeatures(files=None,d=None):
        labels=[]
        if d == None:
            d={"adjPlus":[],
               "adjMinus":[],
               "verbPlus":[],
               "verbMinus":[]}
        
	for key,val in files.items():
	    for textFile in val["files"]:
	        content = readFile([val["path"],textFile])
	        split_sentences = splitter.split(content)
	        postTagged = postagger.pos_tag(split_sentences)
	        wordCount = sum([len(x) for x in postTagged]) 
	        adjectives = [word for sentence in postTagged for word in sentence if "JJ" in word[2]]
	        verbs = [word for sentence in postTagged for word in sentence if "VBZ" in word[2]]
	        allWords = {"adj":adjectives,"verb":verbs}
	        posWords = 0
	        negWords = 0
	
	        for wordKey in allWords:
	            for word in allWords[wordKey]:
	                x = df.loc[df['word'] == word[1]]
	                if not x.empty:
	                    if len(x['pos'].nonzero()[0]) != 0:
	                        posWords += x['pos'].sum()/len(x['pos'].nonzero()[0])
	                    if len(x['neg'].nonzero()[0]) != 0:
	                        negWords += x['neg'].sum()/len(x['neg'].nonzero()[0])
	            d[wordKey+"Plus"].append(posWords/wordCount)
	            d[wordKey+"Minus"].append(negWords/wordCount)
	        labels.append(val["y"])
        return d, labels
 
def arrayFeatures(d):
    return [[w,x,y,z] for w,x,y,z in zip(d["adjPlus"],d["adjMinus"],d["verbPlus"],d["verbMinus"])]



if __name__ == "__main__":
    df, trainFiles, testFiles, splitter, postagger = setup()
    
    trainDict, trainLabels = extractFeatures(trainFiles)#,d="trainDict")
    testDict, _ = extractFeatures(testFiles)#d=testDict)
    trainFeatures = arrayFeatures(trainDict)
    testFeatures = arrayFeatures(testDict)
    clf.fit(X=trainFeatures , y=trainLabels)
    print clf.predict(X=testFeatures)

