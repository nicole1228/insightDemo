
# coding: utf-8

# In[ ]:

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.externals import joblib
import createDB as cDB


# In[6]:


#vec = joblib.load("pickle/vec.pkl")  
#clf = joblib.load("pickle/bernouli.pkl")
#vec = joblib.load("pickle/vecCleaned.pkl")  
#clf = joblib.load("pickle/bernouliCleaned.pkl")
vec = joblib.load("pickle/vecAdjAdv.pkl")  
clf = joblib.load("pickle/bernouliAdjAdv.pkl")
def getSentiment(x):
    vec.set_params(input='content')
    xTest = vec.transform(x)
    y = clf.predict(xTest)
    p = clf.predict_proba(xTest)
    return y,p



# In[ ]:



