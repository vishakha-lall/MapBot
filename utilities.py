from pathlib import Path
def setup_nltk():
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')
#grammar parsing
def parse_sentence(user_input):                                #returns root word, triples of StanfordDependencyParser
    import os
    from nltk.parse.stanford import StanfordDependencyParser
    import config
    path_to_jar = config.stanford_path_to_jar
    path_to_models_jar = config.stanford_path_to_models_jar
    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
    os.environ['JAVAHOME'] = config.javahome
    result = dependency_parser.raw_parse(user_input)
    dep = next(result)                                                          # get next item from the iterator result
    return dep.triples(),dep.root["word"]

#classification into statements questions and chat
def classify_model():
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    FNAME = Path('analysis/featuresDump.csv')
    df = pd.read_csv(filepath_or_buffer = FNAME, )
    df.columns = df.columns[:].str.strip()                                      # Strip any leading spaces from col names
    df['class'] = df['class'].map(lambda x: x.strip())
    width = df.shape[1]
    #split into test and training (is_train: True / False col)
    np.random.seed(seed=1)
    df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
    train, test = df[df['is_train']==True], df[df['is_train']==False]
    features = df.columns[1:width-1]  #remove the first ID col and last col=classifier
    # Fit an RF Model for "class" given features
    clf = RandomForestClassifier(n_jobs=2, n_estimators = 100)
    clf.fit(train[features], train['class'])
    # Predict against test set
    preds = clf.predict(test[features])
    predout = pd.DataFrame({ 'id' : test['id'], 'predicted' : preds, 'actual' : test['class'] })
    return clf

def classify_sentence(clf,user_input):
    import features
    import pandas as pd
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
    myFeatures = features.features_dict('1',user_input, 'X')
    values=[]
    for key in keys:
        values.append(myFeatures[key])
    s = pd.Series(values)
    width = len(s)
    myFeatures = s[1:width-1]  #All but the last item (this is the class for supervised learning mode)
    predict = clf.predict([myFeatures])
    return predict[0].strip()
