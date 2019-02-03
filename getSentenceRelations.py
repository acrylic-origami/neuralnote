import nltk
import os
from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk import Tree
import psycopg2
from nltk.tree import *

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

target = "I know this has already been answered, but I wanted to share a potentially better looking way to call Popen via the use of from x import x and functions."

sub_tree = getSentenceRelations("S" ,target)

root = parser.raw_parse(target)
tree_string = list(root)[0]
tree_string = str(tree_string).replace("\n", "")
tree_string = ' '.join(tree_string.split())
root = Tree.fromstring(tree_string)
list(root)[0].pretty_print()

for item in sub_tree:
	tree = Tree.fromstring(item)
	list(tree)[0].pretty_print()





