import utilities
import databaseconnect
import googleMapsApiModule
from enum import Enum, auto
import logging
import logger_config
from joblib import dump, load
import time
from pathlib import Path
import nltk

location_dict = {"origin": "null", "destination": "null"}

log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)


class LearnResponse(Enum):
    MESSAGE = auto()
    TRAIN_ME = auto()
    ORIGIN = auto()
    DESTINATION = auto()


@logger_config.logger
def setup():
    utilities.setup_nltk()
    logging.debug("NLTK setup completed")

    model_file = "model.joblib"
    retrain = False
    RETRAIN_AFTER_DAYS = 7
    if Path(model_file).exists():
        last_modified_time = Path(model_file).stat().st_mtime
        time_now = time.time()
        diff_in_days = (time_now - last_modified_time) // (86400)
        if diff_in_days < RETRAIN_AFTER_DAYS:
            logging.debug("Loading pre-trained model")
            clf = load(model_file)
        else:
            retrain = True
    else:
        retrain = True
    if retrain:
        logging.debug("Training model")
        clf = utilities.classify_model()
        # clf = utilities.classify_model_adv(model="rf")
        dump(clf, model_file)
    logging.debug("Classification model ready")

    databaseconnect.setup_database()
    logging.debug("Database setup completed, database connected")
    learn_response = LearnResponse.MESSAGE.name
    return clf, learn_response


@logger_config.logger
def message_to_bot(H, clf, learn_response):
    if learn_response == LearnResponse.ORIGIN.name:
        location_dict["origin"] = H
        B = "Can you help me with the destination location?"
        learn_response = LearnResponse.DESTINATION.name
        return B, learn_response
    if learn_response == LearnResponse.DESTINATION.name:
        location_dict["destination"] = H
        origin, destination = (
            location_dict["origin"],
            location_dict["destination"],
        )
        B = googleMapsApiModule.direction(origin, destination)
        learn_response = LearnResponse.MESSAGE.name
        return B, learn_response
    if "bye" in H.lower().split(" "):  # check in words within H
        B = "Bye! I'll miss you!"
        return B, learn_response  # exit loop
    if not H:
        B = "Please say something!"
        return B, learn_response  # empty input

    # grammar parsing
    parts_of_speech = {}
    dependencies = {}
    parsed = utilities.parse_sentence_spacy(H)

    for (text, pos, dep) in parsed:
        parts_of_speech[pos] = text
        dependencies[dep] = text

    root = dependencies["ROOT"]
    subj = [val for key, val in dependencies.items() if "subj" in key]
    obj = [val for key, val in dependencies.items() if "obj" in key]

    verb = [val for key, val in parts_of_speech.items() if "VB" in key]
    adj = [val for key, val in parts_of_speech.items() if "JJ" in key]
    noun = [val for key, val in parts_of_speech.items() if "NN" in key]

    # classification
    classification = utilities.classify_sentence(clf, H)
    # logging.debug(classification)
    if learn_response == LearnResponse.MESSAGE.name:
        databaseconnect.add_to_database(classification, subj, root, verb, H)
        if classification == "C":
            B = databaseconnect.get_chat_response()
        elif classification == "Q":
            B, learn_response = databaseconnect.get_question_response(subj, root, verb)
            if learn_response == LearnResponse.TRAIN_ME.name and (
                len(proper_nouns) == 0
                or (len(proper_nouns) == 1 and H.split(" ", 1)[0] != "Where")
            ):
                databaseconnect.add_learnt_statement_to_database(subj, root, verb)
            if learn_response == LearnResponse.TRAIN_ME.name and (
                len(proper_nouns) >= 2
                or (len(proper_nouns) == 1 and H.split(" ", 1)[0] == "Where")
            ):
                learn_response = LearnResponse.MESSAGE.name
                B = "I will certainly help you with that."
        else:
            B = "Oops! I'm not trained for this yet."
    else:
        B, learn_response = databaseconnect.learn_question_response(H)

    classf_B, classf_learn_response = B, learn_response
    if any(sub in ["distance"] for sub in subj):
        if len(proper_nouns) == 2:
            location_dict["origin"] = proper_nouns.pop(0)
            location_dict["destination"] = proper_nouns.pop(0)
            origin, destination = (
                location_dict["origin"],
                location_dict["destination"],
            )
            B = googleMapsApiModule.direction(origin, destination)
        else:
            B = "I didn't get that. Can you please give me the origin location?"
            learn_response = LearnResponse.ORIGIN.name
    else:
        if len(proper_nouns) == 1:
            location = proper_nouns.pop(0)
        elif compound_NNP:
            location = " ".join(
                word for word in nltk.word_tokenize(H) if word in compound_NNP
            )
        elif len(proper_nouns) == 0:
            location = ""

        API_RESPONSE = False
        if any(sub in ["geocoding", *location.split()] for sub in subj) or root == "is":
            if "map" in noun:
                B = googleMapsApiModule.mapsstatic(location)
                learn_response = LearnResponse.MESSAGE.name
                API_RESPONSE = True
            else:
                B = googleMapsApiModule.geocoding(location)
                learn_response = LearnResponse.MESSAGE.name
                API_RESPONSE = True
        if any(sub in ["elevation", "height", "depth"] for sub in subj) or (
            "high" in adj
        ):
            B = googleMapsApiModule.elevation(location)
            learn_response = LearnResponse.MESSAGE.name
            API_RESPONSE = True
        if any(sub in ["timezone"] for sub in subj) or ("timezone" in adj):
            timezone_name, time_in_tz = googleMapsApiModule.timezone(location)
            B = timezone_name
            learn_response = LearnResponse.MESSAGE.name
            API_RESPONSE = True
        if any(sub in ["time"] for sub in subj):
            timezone_name, time_in_tz = googleMapsApiModule.timezone(location)
            B = time_in_tz
            learn_response = LearnResponse.MESSAGE.name
            API_RESPONSE = True
        if any(nn in ["map"] for nn in noun):
            B = googleMapsApiModule.mapsstatic(location)
            learn_response = LearnResponse.MESSAGE.name
            API_RESPONSE = True
        if not API_RESPONSE:
            try:
                N_places = googleMapsApiModule.places(H)
                B = "\n".join(f"{name}: {link}" for name, link in N_places.items())
                if B == "":
                    B, learn_response = classf_B, classf_learn_response
            except Exception:
                B, learn_response = classf_B, classf_learn_response
            else:
                learn_response = LearnResponse.MESSAGE.name
    return B, learn_response
