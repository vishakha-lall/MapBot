FNAME = 'C:\\Users\\Vishakha Lall\\Projects\\Python\\TestNLTK\\pythonFAQ.csv' # !! Modify this to the CSV data location

import csv
import hashlib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import features

df = pd.read_csv(filepath_or_buffer = FNAME, )
width = df.shape[1]
fin = open(FNAME, 'rt')
reader = csv.reader(fin)
np.random.seed(seed=1)
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
train, test = df[df['is_train']==True], df[df['is_train']==False]
print(str(len(train)), " rows split into training set,", str(len(test)), "split into test set.")

clf = RandomForestClassifier(n_jobs=2, n_estimators = 100)
clf.fit(train[features], train['class'])
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
