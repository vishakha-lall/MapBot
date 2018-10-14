import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

FNAME = 'C:\\Users\\Vishakha Lall\\Projects\\Python\\TestNLTK\\featuresDump.csv'

df = pd.read_csv(filepath_or_buffer = FNAME)
print(str(len(df)), "rows loaded")

df.columns = df.columns[:].str.strip()
df['class'] = df['class'].map(lambda x: x.strip())

width = df.shape[1]

np.random.seed(seed=1)
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
train, test = df[df['is_train']==True], df[df['is_train']==False]
print(str(len(train)), " rows split into training set,", str(len(test)), "split into test set.")

features = df.columns[1:width-1]  #remove the first ID col and last col=classifier
print(f"FEATURES = {features}")
clf = RandomForestClassifier(n_jobs=2, n_estimators = 100)
clf.fit(train[features], train['class'])
preds = clf.predict(test[features])
predout = pd.DataFrame({ 'id' : test['id'], 'predicted' : preds, 'actual' : test['class'] })
print(predout)

## Cross-check accuracy ##
print(pd.crosstab(test['class'], preds, rownames=['actual'], colnames=['preds']))
print("\n",pd.crosstab(test['class'], preds, rownames=['actual']
                       , colnames=['preds']).apply(lambda r: round(r/r.sum()*100,2), axis=1) )

from sklearn.metrics import accuracy_score
print("\n\nAccuracy Score: ", round(accuracy_score(test['class'], preds),3) )


#test model
FNAME = 'C:\\Users\\Vishakha Lall\\Projects\\Python\\TestNLTK\\pythonFAQ.csv' # !! Modify this to the CSV data location

import csv
import hashlib

import features

fin = open(FNAME, 'rt')
reader = csv.reader(fin)

keys = ["id",
"wordCount",
"stemmedCount",
"stemmedEndNN",
"CD",
"NN",
"NNP",
"NNPS",
"NNS",
"PRP",
"VBG",
"VBZ",
"startTuple0",
"endTuple0",
"endTuple1",
"endTuple2",
"verbBeforeNoun",
"qMark",
"qVerbCombo",
"qTripleScore",
"sTripleScore",
"class"]

rows = []

next(reader)  #Assume we have a header
for line in reader:
    sentence = line[0]
    c = line[1]        #class-label
    id = hashlib.md5(str(sentence).encode('utf-8')).hexdigest()[:16] # generate a unique ID

    f = features.features_dict(id,sentence, c)
    row = []

    for key in keys:
        value = f[key]
        row.append(value)
    rows.append(row)

faq = pd.DataFrame(rows, columns=keys)
fin.close()
featureNames = faq.columns[1:width-1]  #remove the first ID col and last col=classifier
faqPreds = clf.predict(faq[featureNames])

predout = pd.DataFrame({ 'id' : faq['id'], 'predicted' : faqPreds, 'actual' : faq['class'] })
print(pd.crosstab(faq['class'], faqPreds, rownames=['actual'], colnames=['preds']))

print("\n",pd.crosstab(faq['class'], faqPreds, rownames=['actual'],
                       colnames=['preds']).apply(lambda r: round(r/r.sum()*100,2), axis=1) )
print("Accuracy Score:", round(accuracy_score(faq['class'], faqPreds) ,3) )
textout = {'Q': "QUESTION", 'C': "CHAT", 'S':"STATEMENT"}

mySentence = "My name is Vishakha"

myFeatures = features.features_dict('1',mySentence, 'X')

values=[]
for key in keys:
    values.append(myFeatures[key])

s = pd.Series(values)
width = len(s)
myFeatures = s[1:width-1]  #All but the last item (this is the class for supervised learning mode)
predict = clf.predict([myFeatures])

print("\n\nPrediction is: ", textout[predict[0].strip()])
