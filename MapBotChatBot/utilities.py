#grammar parsing
def parse_sentence(user_input):                               #returns root word, triples of StanfordDependencyParser
    import os
    from nltk.parse.stanford import StanfordDependencyParser
    path = 'C:\\Users\\Vishakha Lall\\Projects\\Python\\MapBotChatBot\\stanford-corenlp-full-2017-06-09\\'
    path_to_jar = path + 'stanford-corenlp-3.8.0.jar'
    path_to_models_jar = path + 'stanford-corenlp-3.8.0-models.jar'
    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
    os.environ['JAVA_HOME'] = 'C:\\ProgramData\\Oracle\\Java\\javapath'
    result = dependency_parser.raw_parse(user_input)
    dep = next(result)                                                          # get next item from the iterator result
    return dep.triples(),dep.root["word"]

#classification into statements questions and chat
def classify_model():
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    FNAME = 'C:\\Users\\Vishakha Lall\\Projects\\Python\\MapBotChatBot\\analysis\\featuresDump.csv'
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

#setup database
def setup_database():
    import mysql.connector
    db = mysql.connector.connect(user='root',password='viks1995',host='127.0.0.1',database='mapbot')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS chat_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")
    cur.execute("CREATE TABLE IF NOT EXISTS statement_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")
    cur.execute("CREATE TABLE IF NOT EXISTS question_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")

#add classified sentences to database
def add_to_database(classification,subject,root,verb,H):
    import mysql.connector
    db = mysql.connector.connect(user='root',password='viks1995',host='127.0.0.1',database='mapbot')
    cur = db.cursor()
    if classification == 'C':
        cur.execute("INSERT INTO chat_table(subject,root_word,verb,sentence) VALUES (%s,%s,%s,%s)",(str(subject),str(root),str(verb),H))
        db.commit()
    elif classification == 'Q':
        cur.execute("INSERT INTO question_table(subject,root_word,verb,sentence) VALUES (%s,%s,%s,%s)",(str(subject),str(root),str(verb),H))
        db.commit()
    else:
        cur.execute("INSERT INTO statement_table(subject,root_word,verb,sentence) VALUES (%s,%s,%s,%s)",(str(subject),str(root),str(verb),H))
        db.commit()

#get a random chat response
def get_chat_response():
    import mysql.connector
    db = mysql.connector.connect(user='root',password='viks1995',host='127.0.0.1',database='mapbot')
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM chat_table")
    res = cur.fetchone()
    total_chat_records = res[0]
    import random
    chat_id = random.randint(1,total_chat_records+1)
    cur.execute("SELECT sentence FROM chat_table WHERE id = %s" % (int(chat_id)))
    res = cur.fetchone()
    response_sentence = res[0]
    return response_sentence

#get a random chat response
def get_question_response(subject,root,verb):
    import mysql.connector
    db = mysql.connector.connect(user='root',password='viks1995',host='127.0.0.1',database='mapbot')
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM statement_table")
    res = cur.fetchone()
    if res[0] == 0:
        print("Mapbot: I don't know the response to this. Please train me.")
        H = input("You: ")
        cur.execute("INSERT INTO statement_table(subject,root_word,verb,sentence) VALUES (%s,%s,%s,%s)",(str(subject),str(root),str(verb),H))
        db.commit()
        return H
    else:
        cur.execute('SELECT subject FROM statement_table')
        res = cur.fetchall()
        found = 0
        for r in res:
            if r[-1] == str(subject):
                found = 1
                break
        if found == 1:
            if r[-1] == '[]':
                cur.execute('SELECT root_word FROM statement_table')
                res_root = cur.fetchall()
                found_root = 0
                for r_root in res_root:
                    if r_root[-1] == str(root):
                        found_root = 1
                if found_root == 1:
                    cur.execute('SELECT sentence FROM statement_table WHERE root_word="%s"' % (str(root)))
                    res = cur.fetchone()
                    return res[0]
                else:
                    print("Mapbot: I don't know the response to this. Please train me.")
                    H = input("You: ")
                    cur.execute("INSERT INTO statement_table(subject,root_word,sentence) VALUES (%s,%s,%s)",(str(subject),str(root),H))
                    db.commit()
                    return H
            else:
                cur.execute('SELECT verb FROM statement_table WHERE subject="%s"' % (str(subject)))
                res = cur.fetchone()
                if res[0] == str(verb):
                    cur.execute('SELECT sentence FROM statement_table WHERE subject="%s"' % (str(subject)))
                    res = cur.fetchone()
                    return res[0]
                else:
                    print("Mapbot: I don't know the response to this. Please train me.")
                    H = input("You: ")
                    cur.execute("INSERT INTO statement_table(subject,root_word,sentence) VALUES (%s,%s,%s)",(str(subject),str(root),H))
                    db.commit()
                    return H
        else:
            print("Mapbot: I don't know the response to this. Please train me.")
            H = input("You: ")
            cur.execute("INSERT INTO statement_table(subject,root_word,sentence) VALUES (%s,%s,%s)",(str(subject),str(root),H))
            db.commit()
            return H
