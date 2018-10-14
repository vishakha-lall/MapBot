# pass in a sentence, pass out it's features
import nltk
import pandas as pd
import csv
import sys
import hashlib
import re
import string
import itertools
from nltk import word_tokenize
from nltk.corpus import stopwords

lemma = nltk.wordnet.WordNetLemmatizer()
sno = nltk.stem.SnowballStemmer('english')

line = ["xxx","Oracle 12.2 will be released for on-premises users on 15 March 2017",0,"S"]

pos = []           #list of PartsOfSpeech

output = ""        #comma separated string
header = ""        #string for describing features header

VerbCombos = ['VB',
              'VBD',
              'VBG',
              'VBN',
              'VBP',
              'VBZ',
              'WDT',
              'WP',
              'WP$',
              'WRB',
              'MD']

questionTriples = ['CD-VB-VBN',
                   'MD-PRP-VB' ,
                   'MD-VB-CD' ,
                   'NN-IN-DT' ,
                   'PRP-VB-PRP' ,
                   'PRP-WP-NNP' ,
                   'VB-CD-VB' ,
                   'VB-PRP-WP' ,
                   'VBZ-DT-NN' ,
                   'WP-VBZ-DT' ,
                   'WP-VBZ-NNP' ,
                   'WRB-MD-VB']

statementTriples = ['DT-JJ-NN',
                   'DT-NN-VBZ',
                   'DT-NNP-NNP',
                   'IN-DT-NN',
                   'IN-NN-NNS',
                   'MD-VB-VBN',
                   'NNP-IN-NNP',
                   'NNP-NNP-NNP',
                   'NNP-VBZ-DT',
                   'NNP-VBZ-NNP',
                   'NNS-IN-DT',
                   'VB-VBN-IN',
                   'VBZ-DT-JJ']


startTuples = ['NNS-DT',
               'WP-VBZ',
               'WRB-MD']

endTuples = ['IN-NN',
             'VB-VBN',
             'VBZ-NNP']

# Because python dict's return key-vals in random order, provide ordered list to pass to ML models
feature_keys = ["id",
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


def strip_sentence(sentence):
    sentence = sentence.strip(",")
    sentence = ''.join(filter(lambda x: x in string.printable, sentence))  #strip out non-alpha-numerix
    sentence = sentence.translate(str.maketrans('','',string.punctuation)) #strip punctuation
    return(sentence)

def exists_pair_combos(comboCheckList, sentence):
    pos = get_pos(sentence)
    tag_string = "-".join([ i[1] for i in pos ])
    combo_list = []

    for pair in itertools.permutations(comboCheckList,2):
        if(pair[0] == "MD"):  # * Kludge - strip off leading MD *
            pair = ["",""]
        combo_list.append("-".join(pair))

    if any(code in tag_string for code in combo_list):
	    return 1
    else:
        return 0

# Parts Of Speech
def get_pos(sentence):
    sentenceParsed = word_tokenize(sentence)
    return(nltk.pos_tag(sentenceParsed))

# Count Q-Marks
def count_qmark(sentence):
    return(sentence.count("?") )

# Count a specific POS-Type
#VBG = count_POSType(pos,'VBG')
def count_POSType(pos, ptype):
    count = 0
    tags = [ i[1] for i in pos ]
    return(tags.count(ptype))
    #if ptype in tags:
    #    VBG = 1
    #return(VBG)

# Does Verb occur before first Noun
def exists_vb_before_nn(pos):
    pos_tags = [ i[1] for i in pos ]
    #Strip the Verbs to all just "V"
    pos_tags = [ re.sub(r'V.*','V', str) for str in pos_tags ]
    #Strip the Nouns to all just "NN"
    pos_tags = [ re.sub(r'NN.*','NN', str) for str in pos_tags ]

    vi =99
    ni =99
    mi =99

    #Get first NN index
    if "NN" in pos_tags:
        ni = pos_tags.index("NN")
    #Get first V index
    if "V" in pos_tags:
        vi = pos_tags.index("V")
    #get Modal Index
    if "MD" in pos_tags:
        mi = pos_tags.index("MD")

    if vi < ni or mi < ni :
        return(1)
    else:
        return(0)

# Stemmed sentence ends in "NN-NN"?
def exists_stemmed_end_NN(stemmed):
    stemmedEndNN = 0
    stemmed_end = get_first_last_tuples(" ".join(stemmed))[1]
    if stemmed_end == "NN-NN":
        stemmedEndNN = 1
    return(stemmedEndNN)

# Go through the predefined list of start-tuples, 1 / 0 if given startTuple occurs in the list
def exists_startTuple(startTuple):
    exists_startTuples = []
    for tstring in startTuples:  #startTuples defined as global var
        if startTuple in tstring:
            exists_startTuples.append(1)
        else:
            exists_startTuples.append(0)
        return(exists_startTuples)

# Go through the predefined list of end-tuples, 1 / 0 if given Tuple occurs in the list
def exists_endTuple(endTuple):
    exists_endTuples = []
    for tstring in endTuples:    #endTuples defined as global var
        if endTuple in tstring:
            exists_endTuples.append(1)
        else:
            exists_endTuples.append(0)
    return(exists_endTuples)

#loop round list of triples and construct a list of binary 1/0 vals if triples occur in list
def exists_triples(triples, tripleSet):
    exists = []
    for tstring in tripleSet:
        if tstring in triples:
            exists.append(1)
        else:
            exists.append(0)
    return(exists)

# Get a sentence and spit out the POS triples
def get_triples(pos):
    list_of_triple_strings = []
    pos = [ i[1] for i in pos ]  # extract the 2nd element of the POS tuples in list
    n = len(pos)

    if n > 2:  # need to have three items
        for i in range(0,n-2):
            t = "-".join(pos[i:i+3]) # pull out 3 list item from counter, convert to string
            list_of_triple_strings.append(t)
    return list_of_triple_strings

def get_first_last_tuples(sentence):
    first_last_tuples = []
    sentenceParsed = word_tokenize(sentence)
    pos = nltk.pos_tag(sentenceParsed) #Parts Of Speech
    pos = [ i[1] for i in pos ]  # extract the 2nd element of the POS tuples in list

    n = len(pos)
    first = ""
    last = ""

    if n > 1:  # need to have three items
        first = "-".join(pos[0:2]) # pull out first 2 list items
        last = "-".join(pos[-2:]) # pull out last 2 list items

    first_last_tuples = [first, last]
    return first_last_tuples

def lemmatize(sentence):
    """
    pass  in  a sentence as a string, return just core text that has been "lematised"
    stop words are removed - could effect ability to detect if this is a question or answer
    - depends on import lemma = nltk.wordnet.WordNetLemmatizer() and from nltk.corpus import stopwords
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)

    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w.lower())  # also set lowercase
    lem = []
    for w in filtered_sentence:
        lem.append(lemma.lemmatize(w))

    return lem

def stematize(sentence):
    """
    pass  in  a sentence as a string, return just core text stemmed
    stop words are removed - could effect ability to detect if this is a question or answer
    - depends on import sno = nltk.stem.SnowballStemmer('english') and from nltk.corpus import stopwords
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)

    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    stemmed = []
    for w in filtered_sentence:
        stemmed.append(sno.stem(w))

    return stemmed

#########################################################################
# A wrapper function to put it all together - build a csv line to return
# A header string is also returned for optional use
def get_string(id,sentence,c="X"):
    header,output = "",""
    pos = get_pos(sentence)

    qMark = count_qmark(sentence) #count Qmarks before stripping punctuation
    sentence = strip_sentence(sentence)
    #lemmed = lemmatize(sentence)
    stemmed = stematize(sentence)
    wordCount = len(sentence.split())
    stemmedCount = len(stemmed)

    qVerbCombo = exists_pair_combos(VerbCombos,sentence)

    verbBeforeNoun = exists_vb_before_nn(pos)

    output = id + ","  + str(wordCount) + "," + str(stemmedCount) + "," + str(qVerbCombo)+ "," + str(qMark) + "," + str(verbBeforeNoun)
    header = header + "id,wordCount,stemmedCount,qVerbCombo,qMark,verbBeforeNoun"

    # list of POS-TYPES to count , generate a list of counts in the CSV line
    for ptype in ["VBG", "VBZ", "NNP", "NN", "NNS", "NNPS","PRP", "CD" ]:
        output = output + "," + str( count_POSType(pos,ptype) )
        header = header + "," + ptype

    output = output + "," + str(exists_stemmed_end_NN(stemmed))
    header = header + ",StemmedEndNN,"

    ## get Start Tuples and End Tuples Features ##
    startTuple,endTuple = get_first_last_tuples(sentence)

    l = exists_startTuple(startTuple)  #list [1/0] for exists / not exists
    output = output + "," + ",".join(str(i) for i in l)
    for i in range(0,len(l)):
        header = header + "startTuple" + str(i+1) + ","

    l = exists_endTuple(endTuple)  #list [1/0] for exists / not exists
    output = output + "," + ",".join(str(i) for i in l)
    for i in range(0,len(l)):
        header = header + "endTuple" + str(i+1) + ","

    ## look for special Triple Combinations ##
    triples = get_triples(pos)  # all the triple sequences in the sentence POS list

    l = exists_triples(triples, questionTriples)
    total = sum(l)
    output = output + "," + str(total)
    header = header + "qTripleScore" + ","

    l = exists_triples(triples, statementTriples)
    total = sum(l)
    output = output + "," + str(total)
    header = header + "sTripleScore" + ","

    output = output + "," + c  #Class Type on end
    header = header + "class"

    return output,header

# End of Get String wrapper

# Build a dictionary of features
def features_dict(id,sentence,c="X"):
    features = {}
    pos = get_pos(sentence)

    features["id"] = id
    features["qMark"] = count_qmark(sentence) #count Qmarks before stripping punctuation
    sentence = strip_sentence(sentence)
    stemmed = stematize(sentence)
    startTuple,endTuple = get_first_last_tuples(sentence)

    features["wordCount"] = len(sentence.split())
    features["stemmedCount"] = len(stemmed)
    features["qVerbCombo"] = exists_pair_combos(VerbCombos,sentence)
    features["verbBeforeNoun"] = exists_vb_before_nn(pos)

    for ptype in ["VBG", "VBZ", "NNP", "NN", "NNS", "NNPS","PRP", "CD" ]:
        features[ptype] = count_POSType(pos,ptype)

    features["stemmedEndNN"] = exists_stemmed_end_NN(stemmed)

    l = exists_startTuple(startTuple)  #list [1/0] for exists / not exists
    for i in range(0,len(l)):
        features["startTuple" + str(i)] = l[i]

    l = exists_endTuple(endTuple)  #list [1/0] for exists / not exists
    for i in range(0,len(l)):
        features["endTuple" + str(i)] = l[i]

    ## look for special Triple Combinations ##
    triples = get_triples(pos)  # all the triple sequences in the sentence POS list

    l = exists_triples(triples, questionTriples)  # a list of 1/0 for hits on this triple-set
    features["qTripleScore"] = sum(l)  # add all the triple matches up to get a score

    l = exists_triples(triples, statementTriples) # Do same check for the Statement t-set
    features["sTripleScore"] = sum(l)  # add all the triple matches up to get a score

    features["class"] = c  #Class Type on end

    return features

# pass in dict, get back series
def features_series(features_dict):
    values=[]
    for key in feature_keys:
        values.append(features_dict[key])

    features_series = pd.Series(values)

    return features_series

## MAIN ##
if __name__ == '__main__':

    #  ID, WordCount, StemmedCount, Qmark, VBG, StemmedEnd, StartTuples, EndTuples,   QuestionTriples, StatementTriples, Class
    #                                     [1/0] [NN-NN?]    [3 x binary] [3 x binary] [10 x binary]    [10 x binary]

    print("Starting...")

    c = "X"        # Dummy class
    header = ""
    output = ""

    if len(sys.argv) > 1:
        sentence = sys.argv[1]
    else:
        sentence = line[1]

    id = hashlib.md5(str(sentence).encode('utf-8')).hexdigest()[:16]

    features = features_dict(id,sentence, c)
    pos = get_pos(sentence)       #NLTK Parts Of Speech, duplicated just for the printout
    print(pos)

    print(features)
    for key,value in features.items():
        print(key, value)

    #header string
    for key, value in features.items():
       header = header + ", " + key   #keys come out in a random order
       output = output + ", " + str(value)
    header = header[1:]               #strip the first ","" off
    output = output[1:]               #strip the first ","" off
    print("HEADER:", header)
    print("VALUES:", output)
