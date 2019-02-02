import nltk
import os
from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk import Tree
import keyLookup as K
import psycopg2

entity_tokens = ["NN", "NNS", "NNP", "NNPS", "PRP", "PRP$"]

#This function generates the entities from a sentence 
with psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('''
	SELECT
		s.id AS sentence_id,
		p.id AS word_id,
		(ROW_NUMBER() OVER (
			PARTITION BY s.id ORDER BY p.id ASC)
		) AS word_rank,
		word
	FROM (
		SELECT * FROM sentences LIMIT 100
	) s
		INNER JOIN plain p ON p.parent = s.id
		ORDER BY s.id ASC
		LIMIT 1;''')
	row = cur.fetchone()
	D = {}
	entity_state = None # TRow + { word: string[], tag: string[] }
	while row != None:
		sid = row['sentence_id']
		
		if sid not in D:
			D[sid] = []
		tag = nltk.pos_tag(row['word'])
		if tag[1] in entity_tokens:
			D[sid].append((row) + { 'tag': tag[1] })
			
			if entity_state == None:
				entity_state = row
				entity_state['word'] = []
				entity_state['tag'] = []
			entity_state['word'].append(row['word'])
			entity_state['tag'].append(tag)
				
		elif row['word_id'] == 1 and entity_state != None and len(entity['tag']) > 1:
			D[sid].append(entity_state)
		row = cur.fetchone()
	
	D_items = D.items()
	
	W = [np.array(K.model.word_vec(word) if not isinstance(word, list) else np.mean(K.model.word_vec(w) for w in word) for _, word in sentence) for sentence in D_items]
	norms = [[np.linalg.norm(np.matmul(a, b.T)) for sid_b, b in W[i:]] for i, a in enumerate(W)] # consider using determinant but not sensitive to linear dependence, or otherwise understanding the semantics of matrix norm in this context
	# see top 5 max matches branch
	# for i, (sid_l, left) in enumerate(D_items):
	# 	for sid_r, right in D_items[i:]:
	# 		K.model.similarity(left, right)
	
def parseSentence(data):
		
		#Tokenize sent.
		tokens = conn
		
		#Tag sent.
		tagged = nltk.pos_tag(tokens)

		##Generate entities
		entities = []

		#Singular entities 
		i=0
		for word in tagged:
			if word[1] in entity_tokens:
				entities.append([word[0], word[1], i]) #we create (WORD, POS, SENT_INDEX), SENT_INDEX 0 aligned

			i = i + 1

		#Series entities 
		i = 0
		while i < len(tagged):
			
			if tagged[i][1] in entity_tokens:
				length = 1

				j = i + 1
				candidate_phrase = [tagged[i][0]] #add first word to set
				candidate_phrase_tokens = [tagged[i][1]] #add tags
				while j < len(tagged) and tagged[j][1] in entity_tokens:
					candidate_phrase.append(tagged[j][0])
					candidate_phrase_tokens.append(tagged[j][1])
					j = j + 1

				#If we have a run 
				if len(candidate_phrase) > 1:
					entities.append([' '.join(candidate_phrase), ' '.join(candidate_phrase_tokens), i])
					i = j


			i = i + 1

		return entities


#https://stackoverflow.com/questions/13883277/stanford-parser-and-nltk/51981566#51981566
#https://www.nltk.org/book/ch08.html tree key
'''
Symbol	Meaning			Example
S		sentence		the man walked
NP		noun phrase		a dog
VP		verb phrase		saw a park
PP		prepositional phrase	with a telescope
Det		determiner		the
N		noun			dog
V		verb			walked
P		preposition		in
'''

'''

'''

#http://www.surdeanu.info/mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html


def traverse_tree(tree):
    # print("tree:", tree)
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            traverse_tree(subtree)

def parseSentenceStructure(data):

	#Tokenize sent.
	tokens = nltk.word_tokenize(data)

	#Tag sent.
	tagged = nltk.pos_tag(tokens)

	#Parser
	parser = CoreNLPParser(url='http://localhost:9000') #https://stackoverflow.com/questions/13883277/stanford-parser-and-nltk/51981566#51981566
	dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

	#Parse w/ Stanford
	tree = parser.raw_parse(data)
	#print(list(tree))

	list(tree)[0].pretty_print()
	#print(list(tree))

'''
if __name__ == '__main__':
	with psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
		cur = conn.cursor()
		cur.execute('SELECT body FROM documents;')
		for row in cur:
			print(parseSentenceStructure(row[0]))
'''
print(parseSentenceStructure("Dog saw man."))
#"I feel that eggs are the best breakfast food table due to their high protein content."

































