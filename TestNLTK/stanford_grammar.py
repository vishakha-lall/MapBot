import os
from nltk.parse.stanford import StanfordDependencyParser
path = 'C:\\Users\\Vishakha Lall\\Projects\\Python\\TestNLTK\\stanford-corenlp-full-2017-06-09\\'
path_to_jar = path + 'stanford-corenlp-3.8.0.jar'
path_to_models_jar = path + 'stanford-corenlp-3.8.0-models.jar'

dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
os.environ['JAVA_HOME'] = 'C:\\ProgramData\\Oracle\\Java\\javapath'

result = dependency_parser.raw_parse('I shot an elephant in my pajamas')
dep = next(result)  # get next item from the iterator result
for t in dep.triples():
    print(t)
dep.root["word"]
list(dep.tree())
sentence = "He watched the dark eyeslits narrowing with greed till her eyes were green stones"
result = dependency_parser.raw_parse(sentence)
dep = next(result)
print(dep.root["word"])
list(dep.tree())
sentence = "I shot an elephant while I was wearing pyjamas"
result = dependency_parser.raw_parse(sentence)
dep = next(result)
print("Head Word:", dep.root["word"])
