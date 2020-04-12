from pathlib import Path
import logging
import logger_config

log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)


@logger_config.logger
def setup_nltk():
    import nltk

    punkt = nltk.download("punkt")
    averaged_perceptron_tagger = nltk.download("averaged_perceptron_tagger")
    stopwords = nltk.download("stopwords")

    return all((punkt, averaged_perceptron_tagger, stopwords))


@logger_config.logger
# grammar parsing
def parse_sentence(user_input):
    # returns root word, triples of StanfordDependencyParser
    import os
    from nltk.parse.stanford import StanfordDependencyParser
    import config

    path_to_jar = config.stanford_path_to_jar
    path_to_models_jar = config.stanford_path_to_models_jar
    dependency_parser = StanfordDependencyParser(
        path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar
    )
    os.environ["JAVAHOME"] = config.javahome
    result = dependency_parser.raw_parse(user_input)
    dep = next(result)  # get next item from the iterator result
    return dep.triples(), dep.root["word"]


@logger_config.logger
# classification into statements questions and chat
def classify_model():
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier

    FNAME = Path("analysis/featuresDump.csv")
    df = pd.read_csv(filepath_or_buffer=FNAME,)
    df.columns = df.columns[:].str.strip()  # Strip any leading spaces from col names
    df["class"] = df["class"].map(lambda x: x.strip())
    width = df.shape[1]
    # split into test and training (is_train: True / False col)
    np.random.seed(seed=1)
    df["is_train"] = np.random.uniform(0, 1, len(df)) <= 0.75
    train, test = (
        df[df["is_train"] == True],
        df[df["is_train"] == False],
    )  # noqa: E712
    features = df.columns[1 : width - 1]  # noqa: E203
    # remove the first ID col and last col=classifier
    # Fit an RF Model for "class" given features
    clf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    clf.fit(train[features], train["class"])
    # Predict against test set
    preds = clf.predict(test[features])
    predout = pd.DataFrame(  # noqa: F841
        {"id": test["id"], "predicted": preds, "actual": test["class"]}
    )
    # Creates F841 in flake8. Needs to be addressed. `predout` is never used.
    return clf


@logger_config.logger
# classification into statements questions and chat with more choice of ml algorithms parameter tuned by Gridsearchcv.
# By default this uses random forest if no argument passed.by @eaglewarrior
def classify_model_adv(model="rf"):
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from xgboost import XGBClassifier
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.naive_bayes import MultinomialNB

    FNAME = Path("analysis/featuresDump.csv")
    df = pd.read_csv(filepath_or_buffer=FNAME,)
    df.columns = df.columns[:].str.strip()  # Strip any leading spaces from col names
    df["class"] = df["class"].map(lambda x: x.strip())
    width = df.shape[1]
    # split into test and training (is_train: True / False col)
    np.random.seed(seed=1)
    df["is_train"] = np.random.uniform(0, 1, len(df)) <= 0.75
    train, test = (
        df[df["is_train"] == True],
        df[df["is_train"] == False],
    )  # noqa: E712
    features = df.columns[1 : width - 1]  # noqa: E203
    # remove the first ID col and last col=classifier
    # Fit an  Model for "class" given features rf:random forest,xgb:xgboost,nb:naive bayes,ada:adaboost
    if model == "svm":
        clf = SVC(
            C=1000,
            cache_size=200,
            class_weight=None,
            coef0=0.0,
            decision_function_shape="ovr",
            degree=3,
            gamma=0.0001,
            kernel="rbf",
            max_iter=-1,
            probability=False,
            random_state=None,
            shrinking=True,
            tol=0.001,
            verbose=False,
        )
    elif model == "rf":
        clf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    elif model == "xgb":
        clf = XGBClassifier(learning_rate=0.01, n_estimators=500)
    elif model == "nb":
        clf = MultinomialNB()
    # best performance by adaboost
    elif model == "ada":
        clf = AdaBoostClassifier(learning_rate=0.001, n_estimators=2000)
    clf.fit(train[features], train["class"])
    # Predict against test set
    preds = clf.predict(test[features])
    predout = pd.DataFrame(  # noqa: F841
        {"id": test["id"], "predicted": preds, "actual": test["class"]}
    )
    # Creates F841 in flake8. Needs to be addressed. `predout` is never used.
    return clf


@logger_config.logger
def classify_sentence(clf, user_input):
    import features
    import pandas as pd

    keys = [
        "id",
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
        "class",
    ]
    myFeatures = features.features_dict("1", user_input, "X")
    values = []
    for key in keys:
        values.append(myFeatures[key])
    s = pd.Series(values)
    width = len(s)
    myFeatures = s[1 : width - 1]  # noqa: E203
    # All but the last item (this is the class for supervised learning mode)
    predict = clf.predict([myFeatures])
    return predict[0].strip()
