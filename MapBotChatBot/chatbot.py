from utilities import parse_sentence
from utilities import classify_model
from utilities import classify_sentence

clf = classify_model()

B = "Hi! I'm Mapbot!"
while True:
    print('Mapbot: '+B)
    H = input("You: ")
    if H == "":                                                                 #empty input
        B = "Bye! I'll miss you!"
        print('Mapbot: '+B)
        break                                                                   #exit loop
    #grammar parsing
    triples,root = parse_sentence(H)
    triples = list(triples)
    for t in triples:
        relation = t[1]
        if relation[-4:] == 'subj':
            subj = t[2][0]
        if relation[-3:] == 'obj':
            obj = t[2][0]
    #print("\t"+"Subject: "+str(subj)+"\n"+"\t"+"Object: "+str(obj)+"\n"+"\t"+"Topic: "+str(root))
    #classification
    classify_sentence(clf,H)
