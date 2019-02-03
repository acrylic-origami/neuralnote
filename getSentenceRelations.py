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

