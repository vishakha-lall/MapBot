# Use the features.py module to dump out features
# read in a CSV of sentences and bulk-dump to dump.csv of features
# Input CSV fmt:  1st field is sentence ID, 2nd field is text to process, 3rd field is class
import csv
import sys
import hashlib
from pathlib import Path
import features  # features.py is bepoke util to extract NLTK POS features from sentences
import logging

log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)

if len(sys.argv) > 1:
    FNAME = Path(sys.argv[1])
else:
    FNAME = Path("./analysis/sentences.csv")
logging.debug("reading input from ", FNAME)


if len(sys.argv) > 2:
    FOUT = Path(sys.argv[2])
else:
    FOUT = Path("./analysis/featuresDump.csv")
logging.debug("Writing output to ", FOUT)


fin = open(FNAME, "rt")
fout = open(FOUT, "wt", newline="")

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

reader = csv.reader(fin)

loopCount = 0
next(reader)  # Assume we have a header
for line in reader:
    sentence = line[0]
    c = line[1]  # class-label
    id = hashlib.md5(str(sentence).encode("utf-8")).hexdigest()[:16]
    # generate a unique ID

    output = ""
    header = ""

    # get header and string output
    # output, header = features.get_string(id,sentence,c)
    f = features.features_dict(id, sentence, c)

    for key in keys:
        value = f[key]
        header = header + ", " + key
        output = output + ", " + str(value)

    if loopCount == 0:  # only extract and print header for first dict item
        header = header[1:]  # strip the first ","" off
        logging.debug(header)
        fout.writelines(header + "\n")

    output = output[1:]  # strip the first ","" off

    loopCount = loopCount + 1
    logging.debug(output)
    fout.writelines(output + "\n")

fin.close()
fout.close()
