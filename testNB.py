
# coding: utf-8

# In[1]:

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.metrics import roc_auc_score
import pandas as pd
import os
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.externals import joblib


# In[2]:

def setup(numFiles = None):

    posPath = "testReviews/txt_sentoken/pos/"
    negPath = "testReviews/txt_sentoken/neg/"
    max = numFiles
    #trainFiles = {"pos": {"files" : os.listdir(posPath+"/train/")[:max],
    #                      "path" : posPath+"/train/",
    #                      "y" : 1},
    #              "neg": {"files" : os.listdir(negPath+"/train/")[:max],
    #                      "path" : negPath+"/train/",
    #                      "y" : 0}}

    #testFiles = {"pos": {"files" : os.listdir(posPath+"/test/")[:max/4],
    #                     "path" : posPath+"/test/",
    #                     "y" : 1},
    #             "neg": {"files" : os.listdir(negPath+"/test/")[:max/4],
    #                     "path" : negPath+"/test/",
    #                     "y" : 0}
                 
    #trainFiles = {"pos": {"files" : os.listdir(posPath+"/train/cleaned/")[:max],
    #                      "path" : posPath+"/train/cleaned/",
    #                      "y" : 1},
    #              "neg": {"files" : os.listdir(negPath+"/train/cleaned/")[:max],
    #                      "path" : negPath+"/train/cleaned/",
    #                      "y" : 0}}

    #testFiles = {"pos": {"files" : os.listdir(posPath+"/test/cleaned/")[:max/4],
    #                     "path" : posPath+"/test/cleaned/",
    #                     "y" : 1},
    #             "neg": {"files" : os.listdir(negPath+"/test/cleaned/")[:max/4],
    #                     "path" : negPath+"/test/cleaned/",
    #                     "y" : 0}

    #             }
    trainFiles = {"pos": {"files" : os.listdir(posPath+"/train/adj_adv/")[:max],
                          "path" : posPath+"/train/adj_adv/",
                          "y" : 1},
                  "neg": {"files" : os.listdir(negPath+"/train/adj_adv/")[:max],
                          "path" : negPath+"/train/adj_adv/",
                          "y" : 0}}

    testFiles = {"pos": {"files" : os.listdir(posPath+"/test/adj_adv/")[:max/4],
                         "path" : posPath+"/test/adj_adv/",
                         "y" : 1},
                 "neg": {"files" : os.listdir(negPath+"/test/adj_adv/")[:max/4],
                         "path" : negPath+"/test/adj_adv/",
                         "y" : 0}

                 }
    return trainFiles, testFiles


# In[22]:

if __name__ == "__main__":
    
    max = 799

    trainFiles, testFiles = setup(numFiles=max)
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.1,
                                 stop_words='english',
                                 input='filename',
                                 max_features=1000,
                                 #ngram_range=(1,1)
                                 )
   
    print len([trainFiles["neg"]["path"]+x for x in trainFiles["neg"]["files"]])#+
                                      #[trainFiles["neg"]["path"]+x for x in trainFiles["neg"]["files"]])
    xTrain = vectorizer.fit_transform([trainFiles["pos"]["path"]+x for x in trainFiles["pos"]["files"]]+
                                      [trainFiles["neg"]["path"]+x for x in trainFiles["neg"]["files"]])
    xTest = vectorizer.transform([testFiles["pos"]["path"]+x for x in testFiles["pos"]["files"]]+
                                      [testFiles["neg"]["path"]+x for x in testFiles["neg"]["files"]])

    
    clf =BernoulliNB(alpha=.01)
    #clf = MultinomialNB(alpha=.01)
  
    clf.fit(xTrain, [1]*max+[0]*max)
    print xTest.get_shape()
    y_score = clf.predict(xTest)
    y_prob = clf.predict_proba(xTest)
    y_test=[1]*199+[0]*199
    scores=clf.score(xTest,[1]*199+[0]*199)
    #scores=clf.score(y_prob[:,0],[1]*200+[0]*200)
    print roc_auc_score([1]*199+[0]*199, y_prob[:,1], average='macro', sample_weight=None)
    #from sklearn.externals import joblib
    joblib.dump(clf, 'pickle/bernouliAdjAdv.pkl')
    joblib.dump(vectorizer, 'pickle/vecAdjAdv.pkl')
  


# In[7]:

fpr = dict()
tpr = dict()
roc_auc = dict()
print 0
fpr, tpr, _ = roc_curve([1]*200+[0]*200, y_prob[:,1])
print fpr
print tpr
roc_auc = auc(fpr, tpr)
print y_score.ravel()
# Compute micro-average ROC curve and ROC area
#fpr["micro"], tpr["micro"], _ = roc_curve(y_test, y_score.ravel())
#roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

# Plot of a ROC curve for a specific class
plt.figure()
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()

# Plot ROC curve
#plt.figure()
#plt.plot(fpr["micro"], tpr["micro"],
#         label='micro-average ROC curve (area = {0:0.2f})'
#               ''.format(roc_auc["micro"]))
#for i in range(1):
#    plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'
#                                   ''.format(i, roc_auc[i]))#

#plt.plot([0, 1], [0, 1], 'k--')
#plt.xlim([0.0, 1.0])
#plt.ylim([0.0, 1.05])
##plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive Rate')
#plt.title('Some extension of Receiver operating characteristic to multi-class')
#plt.legend(loc="lower right")
#plt.show()


# In[ ]:




# In[ ]:



