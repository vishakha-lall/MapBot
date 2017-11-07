import nltk
nltk.download("reuters") # Reuters Corpus
nltk.download('punkt') # Punkt Tokenizer Model
nltk.download('averaged_perceptron_tagger') # Part-of-Speech Tokeniser
nltk.download("stopwords") # Stopwords

from nltk.corpus import reuters
categories = reuters.categories()
print("Number of Categories:",len(categories))
print(categories[1:9],categories[-10:])

words = reuters.words()
print("number of words", len(words) )
print("first 10 words:", words[0:9])

#Extract at a specific category
tradeWords = reuters.words(categories = 'trade')
print(len(tradeWords))

#remove stopwords and punctuation
from nltk.corpus import stopwords
import string
print(stopwords.words('english'))
tradeWords = [w for w in tradeWords if w.lower() not in stopwords.words('english') ]
tradeWords = [w for w in tradeWords if w not in string.punctuation]
punctCombo = [c+"\"" for c in string.punctuation ]+ ["\""+c for c in string.punctuation ]
tradeWords = [w for w in tradeWords if w not in punctCombo]
print(len(tradeWords))
