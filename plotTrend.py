
# coding: utf-8

# In[1]:


import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from sentResults import pointsToPlot
import matplotlib.dates as dates
get_ipython().magic(u'matplotlib inline')



# In[2]:

matplotlib.rcParams.update({'font.size': 22})


# In[4]:

fig = plt.figure(figsize=(16,6))
x = []
y = []
l = []
t = []
for points in pointsToPlot:
    x.append(dates.datestr2num(datetime.datetime.strptime(points[0], '%Y-%m-%d').strftime('%m/%d/%y')))
    y.append(points[1])
    l.append(points[4])
    t.append(points[5])

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())
plt.plot(x,y,lw=0,marker='o')
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.ylabel('Score')
plt.xlabel('Date')
fig.savefig('test2png.png', dpi=100, forward=True)


# In[ ]:

fig = plt.figure(figsize=(10,10))

plt.plot(l,y,lw=0,marker='o')
plt.ylabel('Score')
plt.xlabel('word count in Article')
fig.savefig('wordCountVsScorepng', dpi=100, forward=True)


# In[ ]:

pos = 3941.39
neg = 5041.06
fig, ax = plt.subplots()
rects1 = plt.bar(0, pos, .35,
                 alpha=.4,
                 color='b',
                 label='Positive Weights')

rects2 = plt.bar(.35 , neg, .35,
                 alpha=.4,
                 color='r',
                 label='Negative Weights')
plt.xlabel('Words')
plt.ylabel('Weight')
plt.title('Word Bank Weights')
plt.xticks((0.35,), ['Pos               Neg'])
fig.savefig('wordBankWeights', dpi=200, forward=True)


# In[7]:

fig = plt.figure(figsize=(10,10))

plt.plot(t,y,lw=0,marker='o')
plt.ylabel('score on truncated article')
plt.xlabel('score on full article')
plt.plot([-5,20],[-5,20])
fig.savefig('scoreVsScore', dpi=200, forward=True)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



