# MapBot
The project aims to give users a new way to interact with Google Maps by building engaging text-based conversational interfaces. Using Natural Language Processing, it analyses the user's intent and responds in the most useful way.

## TestBlog
**Week 2 LITG**   
A blog example created using Django.
The blog provides functionality of viewing blog posts, adding new blog posts and editing existing blog posts. It also includes security features so that changes can be made only by an authenticated user.

## SimpleBot
**Week 3 LITG**  
SimpleBot is a toy chatbot developed in Python with a mySQL database backend. The bot stores a table of word associations for responses to a previous sentence and uses this to match future responses.
It learns from the previous conversation with the user. It maintains a database of previous replies to the same questions and responds based on queries from the database. 
It does not extract the meaning of sentences written by the user. When the user types a message, it is understood as an answer to previous statement made by the chatbot. The sentence typed by the user will then be associated with the words present in the previous message. The human message is decomposed in words. The program will try to identify which sentences correspond best to those words, according to its previous “experience”.
The limitations of the SimpleBot are the motivation for using NLP and ML.

## TestNLTK
**Week 4 LITG**  
Python NLTK  
Stanford CoreNLP  
Illustraions to understand basic NLP functionalities  
* Exploring corpora and treebanks
* Tokenisation of text and parts of speech
* Grammar structure and dependency trees
* Classification of sentences using ML

## TestMapsAPI
**Week 4 LITG**   
Google Maps API  
Exploring functionalities
* Geocoding a location
* Reverse geocoding
* Directions between 2 locations
* Distance matrix between multiple locations
* Searching for a nearby location

## MapBotChatBot
An improvement over SimpleBot to enhance conversation between the user and Mapbot.  
* User input
* Grammar tokenisation using Standford NLP
  * Extract root word
  * Extract subject word and subject list(for compound entities)
  * Extract object word and object list(for compound entities)
  * Extract all proper nouns(location details)
  * Extract verb
* Classification of sentence into Statement, Question and Chat entity using feature extractor ML model
* Store in database depending on the sentence type
* Respond question with corresponding statement query
* Respont chat with chat query

## Python Library Dependencies
* numpy 1.13.3
* pandas 0.21.0
* scikit-learn 0.19.1
* googlemaps 2.5.1
* django 1.11.8
* urllib3 1.22

## Files and Components
* features.py Feature Generator
  This Python module extracts features from a sentence.
  The features.py module includes a function
     get_triples(pos)
  which returns a string of the form "POS-POS-POS" where "POS" is a Part-Of-Speech tag.
* featuresDump.csv is a dump of features extracted from the sentences.csv using the Feature Generator. This data is then used to train a Random Forrest Model to classify a sentence as a Chat, Statement or Question. The Question and Statement predictions are reported as greater than 80% accurate and the features extraction method could easily be expanded on and enhanced.
Also the training data-set is small. 
