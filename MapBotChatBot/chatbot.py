from utilities import parse_sentence
from utilities import classify_model
from utilities import classify_sentence
from utilities import setup_database
from utilities import add_to_database
from utilities import get_chat_response
from utilities import get_question_response

clf = classify_model()
setup_database()

B = "Hi! I'm Mapbot!"
while True:
    print('Mapbot: '+B)
    H = input("You: ")
    if H == "":                                                                 #empty input
        B = "Bye! I'll miss you!"
        print('Mapbot: '+B)
        break                                                                   #exit loop
    #grammar parsing
    subj = set()
    obj = set()
    verb = set()
    triples,root = parse_sentence(H)
    triples = list(triples)
    for t in triples:
        if t[0][1][:2] == 'VB':
            verb.add(t[0][0])
        relation = t[1]
        if relation[-4:] == 'subj':
            subj.add(t[2][0])
        if relation[-3:] == 'obj':
            obj.add(t[2][0])
    #print("\t"+"Subject: "+str(subj)+"\n"+"\t"+"Object: "+str(obj)+"\n"+"\t"+"Topic: "+str(root)+"\n"+"\t"+"Verb: "+str(verb))
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
    #print("\t"+"Proper Nouns: "+str(proper_nouns))
    #classification
    classification = classify_sentence(clf,H)
    #print(classification)
    add_to_database(classification,subj,root,verb,H)
    if classification == 'C':
        B = get_chat_response()
    elif classification == 'Q':
        B = get_question_response(subj,root,verb)
