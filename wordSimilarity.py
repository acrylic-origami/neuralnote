#https://stackoverflow.com/questions/42986405/how-to-speed-up-gensim-word2vec-model-load-time/43067907
import nltk
import os
from gensim.models import KeyedVectors
from threading import Semaphore
from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk import Tree

#Load Model
model = KeyedVectors.load('/home/data/word2vec_models/glove.6B.300d.model', mmap='r')
model.syn0norm = model.syn0  # prevent recalc of normed vectors
#model.most_similar('stuff')  # any word will do: just to page all in
#print(model.similarity("eggs", "egg"))

#Load servers
parser = CoreNLPParser(url='http://localhost:9000') #https://stackoverflow.com/questions/13883277/stanford-parser-and-nltk/51981566#51981566
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

def getSentenceRelations(query, data):

	#Run Parser
	tree = parser.raw_parse(data)
	tree_string = list(tree)[0]
	tree_string = str(tree_string).replace("\n", "")
	tree_string = ' '.join(tree_string.split())

	#Put string to temp file
	f=open("TEMPFILE_TREE","w+")
	f.write(tree_string)
	f.close()

	#Run script
	#output = os.system("./tregex/tregex.sh 'NP' TEMPFILE_TREE")
	output = os.popen("./tregex/tregex.sh '"+query+"' TEMPFILE_TREE").read()

	arr = output.split("\n")

	#print(tree_string)

	sub_trees = [""]
	i = 0
	for item in arr:
		if len(item) < 1:
			i = i + 1
			sub_trees.append("")
		else:
			sub_trees[i] = sub_trees[i] + " " + item

	i = 0
	for item in sub_trees:
		sub_trees[i] = ' '.join(item.split())
		i = i + 1

	sub_trees = [t for t in sub_trees if t != '']

	return sub_trees



def tree_recurse(parent, level=0):
	output = []
	for child in parent:
		if isinstance(child, nltk.Tree):
			output.append(tree_recurse(child))

		else: #we have reached the end
			#parent.label() #"PRP"
			return child

	return " ".join(output)


#Given two sentences, which aspects of sent_display should we highlight 
#	given the shaddow sentence topic. 
def sigWords(sent_display, sent_shaddow):

	#Process: 1) get entities processed out, 2) word embedding similarity to other sent.

	#DIsplay root tre
	tree = parser.raw_parse(sent_display)
	list(tree)[0].pretty_print()

	sub_trees = getSentenceRelations("NP", sent_display)
	subject_entities = []

	for item in sub_trees:
		tree = Tree.fromstring(item)
		list(tree)[0].pretty_print()

		subject = tree_recurse(list(tree)[0])
		subject_entities.append(subject)


	print(subject_entities)


#Ideally hike through the forst is highlighted
sigWords("It was a bright day and I decided to go for a hike through the forest, what good exercise.", "Swimming is the best way to work your body out.")

















