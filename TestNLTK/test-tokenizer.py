import nltk
nltk.download('punkt')
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
sample_text="Harry Potter and the Philosopher's Stone is the first novel in the Harry Potter series. The book was first published on 26 June, 1997[1] by Bloomsbury in London, and was later made into a film of the same name. Both the book and motion picture were released in the United States under the name Harry Potter and the Sorcerer's Stone, because the publishers were concerned that most American readers would not be familiar enough with the term Philosopher's Stone. However this discussion lead to criticism by the British public who felt as if it shouldn't be changed due to the fact it was an English book."
tokens=nltk.sent_tokenize(sample_text)
for x in tokens:
    print(">",x)

from nltk import word_tokenize

sentence = "Mary had a little lamb it's fleece was white as snow."
# Default Tokenisation
tree_tokens = word_tokenize(sentence)

# Other Tokenisers
punct_tokenizer = nltk.tokenize.WordPunctTokenizer()
punct_tokens = punct_tokenizer.tokenize(sentence)

space_tokenizer = nltk.tokenize.SpaceTokenizer()
space_tokens = space_tokenizer.tokenize(sentence)

print("DEFAULT: ", tree_tokens)
print("PUNCT  : ", punct_tokens)
print("SPACE  : ", space_tokens)

#POS tagging
pos = nltk.pos_tag(tree_tokens)
print(pos)
pos_space = nltk.pos_tag(space_tokens)
print(pos_space)

#stemming
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
snowball = nltk.stem.snowball.SnowballStemmer("english")

print([porter.stem(t) for t in tree_tokens])
print([lancaster.stem(t) for t in tree_tokens])
print([snowball.stem(t) for t in tree_tokens])

sentence2 = "When I was going into the woods I saw a bear lying asleep on the forest floor"
tokens2 = word_tokenize(sentence2)

print("\n",sentence2)
for stemmer in [porter, lancaster, snowball]:
    print([stemmer.stem(t) for t in tokens2])

#lemmatizing
wnl = nltk.WordNetLemmatizer()
tokens2_pos = nltk.pos_tag(tokens2)  #nltk.download("averaged_perceptron_tagger")

print([wnl.lemmatize(t) for t in tree_tokens])

print([wnl.lemmatize(t) for t in tokens2])
