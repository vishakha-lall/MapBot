import utilities
import databaseconnect
import googleMapsApiModule  
import logging
import logger_config
location_dict = {"origin": "null", "destination": "null"}

log = logging.getLogger(__name__)
log.info('Entered module: %s' % __name__)


@logger_config.logger
def setup():
    utilities.setup_nltk()
    logging.debug('NLTK setup completed')
    clf = utilities.classify_model()
    logging.debug('Classification model ready')
    databaseconnect.setup_database()
    logging.debug('Database setup completed, database connected')
    learn_response = 0
    return clf, learn_response


@logger_config.logger
def message_to_bot(H, clf, learn_response):
    if learn_response == 2:
        location_dict["origin"] = H
        B = "Can you help me with the destination location?"
        learn_response = 3
        return B, learn_response
    if learn_response == 3:
        location_dict["destination"]=H
        origin, destination = location_dict["origin"], location_dict["destination"]
        googleMapsApiModule.direction(origin,destination)
        B = "I will certainly help you with that."
        learn_response = 0
        return B, learn_response
    if "bye" in H.lower().split(" "):       #check in words within H   
        B = "Bye! I'll miss you!"
        return B, learn_response      # exit loop
    if not H:
        B = "Please say something!" 
        return B, learn_response          #empty input
    # grammar parsing   
    subj = set()
    obj = set()
    verb = set()
    triples,root = utilities.parse_sentence(H)
    triples = list(triples)
    for t in triples:
        if t[0][1][:2] == 'VB':
            verb.add(t[0][0])
        relation = t[1]
        if relation[-4:] == 'subj':
            subj.add(t[2][0])
        if relation[-3:] == 'obj':
            obj.add(t[2][0])
    logging.debug("\t"+"Subject: "+str(subj)+"\n"+"\t"+"Object: "+str(obj)+"\n"+"\t"+"Topic: "+str(root)+"\n"+"\t"+"Verb: "+str(verb))
    subj = list(subj)
    obj = list(obj)
    verb = list(verb)
    proper_nouns = set()
    for t in triples:
        if t[0][1] == 'NNP':
            proper_nouns.add(t[0][0])
        if t[2][1] == 'NNP':
            proper_nouns.add(t[2][0])
    proper_nouns == list(proper_nouns)
    logging.debug("\t"+"Proper Nouns: "+str(proper_nouns))
    #classification
    classification = utilities.classify_sentence(clf,H)
    #logging.debug(classification)
    if learn_response == 0:
        databaseconnect.add_to_database(classification, subj, root, verb, H)
        if (classification == 'C'):
            B = databaseconnect.get_chat_response()
        elif (classification == 'Q'):
            B, learn_response = databaseconnect.get_question_response(subj, root, verb)
            if learn_response == 1 and (len(proper_nouns) == 0 or (len(proper_nouns) == 1 and H.split(" ", 1)[0] != "Where")):
                databaseconnect.add_learnt_statement_to_database(subj, root, verb)
            if learn_response == 1 and (len(proper_nouns) >= 2 or (len(proper_nouns) == 1 and H.split(" ", 1)[0] == "Where")):
                learn_response = 0
                B = "I will certainly help you with that."
        else:
            B = "Oops! I'm not trained for this yet."
    else:
        B, learn_response = databaseconnect.learn_question_response(H)
    if (len(proper_nouns) >= 2 or (len(proper_nouns) >= 1 and H.split(" ", 1)[0] == "Where")) and len(subj) != 0:
        if subj[0] == "distance":
            if len(proper_nouns) == 2:
                location_dict["origin"] = proper_nouns.pop()
                location_dict["destination"] = proper_nouns.pop()
                origin, destination = location_dict["origin"], location_dict["destination"]
                googleMapsApiModule.direction(origin,destination)
            else:
                B = "I didn't get that. Can you please give me the origin location?"
                learn_response = 2
        if len(proper_nouns) == 1:
            location = proper_nouns.pop()
            if subj[0] == "geocoding" or subj[0] == location:
                googleMapsApiModule.geocoding(location)
                learn_response = 0
                B = "I will certainly help you with that."
    return B, learn_response
