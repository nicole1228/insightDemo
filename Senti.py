import pprint
import urllib
from cleanedDict2 import rows as dictRows
from nlpHelpers import Splitter, POSTagger, DictionaryTagger#, sentiment_score
from nltk.stem.wordnet import WordNetLemmatizer
from newspaper import Article
import math
import os

splitter = Splitter()
postagger = POSTagger()

nouns = ["NN","NNS"]
verbs = ["VB","VBD","VBG","VBN","VBP","VBZ"]
adj = ["JJ","JJS","JJR"]
adv = ["RBR","RBS"]
def setup(numFiles = None):


    posPath = "testReviews/txt_sentoken/pos/"
    negPath = "testReviews/txt_sentoken/neg/"
    max = numFiles
    trainFiles = {"pos": {"files" : os.listdir(posPath+"/train/")[:max],
                          "path" : posPath+"/train/",
                          "y" : 1},
                  "neg": {"files" : os.listdir(negPath+"/train/")[:max],
                          "path" : negPath+"/train/",
                          "y" : 0}}

    testFiles = {"pos": {"files" : os.listdir(posPath+"/test/")[:max/4],
                         "path" : posPath+"/test/",
                         "y" : 1},
                 "neg": {"files" : os.listdir(negPath+"/test/")[:max/4],
                         "path" : negPath+"/test/",
                         "y" : 0}

                 }
    return trainFiles, testFiles

if __name__ == "__main__":    

    max = 800

    trainFiles, testFiles = setup(numFiles=max)
    catTup = (trainFiles, testFiles)
    for split in catTup:
        for cats in split:
            for i,tFiles in enumerate(split[cats]["files"]):
                path = split[cats]["path"]+tFiles
                print path
                if not os.path.isfile(path): continue
                f = open(path,"r")
                text = f.read()
                f.close()
                outF = open(path.replace(".txt","_adj_adv.txt"), "w")
                splitted_sentences = splitter.split(text)
                pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
                wordList=[]
                for sentence in pos_tagged_sentences:
                    for word in sentence:
                        #if word[2][0] in nouns+verbs+adj:
                        if word[2][0] in adj+adv:
                            wordList.append(word[0])
                print " ".join(wordList)
                outF.write(" ".join(wordList))
                outF.close()
                print i,cats
	
            
