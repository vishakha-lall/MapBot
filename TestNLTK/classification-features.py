import numpy as np
import pandas as pd
import sys
import features

CODE_LOC = 'C:\\Users\\Vishakha Lall\\Projects\\Python\\TestNLTK'
DATA_LOC = 'C:\\Users\\Vishakha Lall\\Projects\\Python\\TestNLTK\\sentences.csv'

sentences = pd.read_csv(filepath_or_buffer = DATA_LOC)
print(sentences.head(10))

sentence = "Can a dog see in colour?"

sentence = features.strip_sentence(sentence)
print(sentence)
pos = features.get_pos(sentence)
triples = features.get_triples(pos)

print(triples)
sentences = ["Can a dog see in colour?",
             "Hey, How's it going?",
             "Oracle 12.2 will be released for on-premises users on 15 March 2017",
             "When will Oracle 12 be released"]
id = 1
for s in sentences:
    features_dict = features.features_dict(str(id),s)
    features_string,header = features.get_string(str(id),s)
    print(features_dict)
    #print(features_string)
    id += 1
