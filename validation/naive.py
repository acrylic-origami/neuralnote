import numpy as np
# from .. import keyLookup as K
import psycopg2
import psycopg2.extras
import nltk
import traceback
import sys

from functools import reduce
from gensim.models import KeyedVectors
from threading import Semaphore

TOP = 5

#Load Model
model = KeyedVectors.load('/home/data/word2vec_models/glove.6B.300d.model', mmap='r')
model.syn0norm = model.syn0  # prevent recalc of normed vectors
# eff relative imports >_>

entity_tokens = set(["NN", "NNS", "NNP", "NNPS", "PRP", "PRP$"])
# This function generates the entities from a sentence 
def run():
	with psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute('''
		SELECT
			s.id AS sentence_id,
			p.id AS word_id,
			(ROW_NUMBER() OVER (
				PARTITION BY s.id ORDER BY p.id ASC)
			) AS word_rank,
			p.word,
			p.label as tag
		FROM (
			SELECT * FROM sentences LIMIT 100
		) s
			INNER JOIN plain p ON p.sentence = s.id
			WHERE p.word IS NOT NULL AND p.word <> ''
			ORDER BY s.id ASC;''')
		'''
			SELECT s.*, st0.c FROM test.rtree tt
				INNER JOIN test.rsentence ts ON ts.r_cid = tt.child
				INNER JOIN sentences s ON s.id = ts.sentence
				INNER JOIN (SELECT COUNT(*) c, tt.root FROM test.rtree AS tt GROUP BY tt.root LIMIT 10) st0 ON st0.c > 30 AND st0.root = tt.root
		'''
		
		D = {}
		entity_state = None # TRow + { word: string[], tag: string[] }
		for row in cur:
			sid = row['sentence_id']
			
			try:
				# print(row['word'], row['tag'])
				if row['tag'] in entity_tokens and row['word'].lower() in model:
					if sid not in D:
						D[sid] = []
					D[sid].append(dict(row))
					
					if entity_state == None:
						entity_state = dict(row)
						entity_state['word'] = []
						entity_state['tag'] = []
					entity_state['word'].append(row['word'])
					entity_state['tag'].append(row['tag'])
						
				elif row['word_id'] == 1 and entity_state != None and len(entity_state['tag']) > 1:
					D[sid].append(entity_state)
					entity_state = None
			except (KeyboardInterrupt, SystemExit):
				raise
			except:
				# raise
				conn.rollback()
				print(traceback.print_exc())
		
		D_items = D.items()
		
		W = [(sid, [model.word_vec(word['word'].lower()) if not isinstance(word['word'], list) else np.mean([model.word_vec(w) for w in word['word']]) for word in sentence]) for sid, sentence in D_items]
		# norms = [[np.array([reduce(lambda acc, b: acc + [np.linalg.norm(np.matmul(a, b))], [b for b in t if not isinstance(b, list)], []) for a in s]) for t in W[i:]] for i, s in enumerate(W)] # consider using determinant but not sensitive to linear dependence, or otherwise understanding the semantics of matrix norm in this context
		print('PROCESSING %d words' % len(W))
		norms = [[np.asscalar(np.linalg.norm(np.matmul(s, np.array(t).T))) for _, t in W[i:]] for i, (_, s) in enumerate(W)]
		np_norms = [np.array([norms[j][i-j] for j in range(i-1)] + n) for i, n in enumerate(norms)]

# def runb():
# 	with psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
# 		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
# 		np_norms = np.load('np_norms.npz.npy')
# 		W = np.load('W.npz.npy')
		for i, row in enumerate(np_norms):
			sys.stdout.write('\r%d' % i)
			top_rows = row.argsort()[-TOP:].tolist()
			
			cur.execute('CREATE TEMPORARY TABLE _top_sentences ( sentence INT ) ON COMMIT DROP;')
			cur.execute('INSERT INTO _top_sentences VALUES %s' % ('(%s),' * TOP)[:-1], top_rows)
			cur.execute('''
				WITH RECURSIVE r (parent, match) AS (
					SELECT ts.r_cid, top_s.sentence FROM test.rsentence ts
						LEFT JOIN _top_sentences top_s ON top_s.sentence = ts.sentence
						WHERE ts.sentence = %s
					UNION
					SELECT tt.child, top_s.sentence FROM r
						INNER JOIN test.rtree tt ON tt.parent = r.parent
						INNER JOIN test.rsentence tr ON tr.r_cid = tt.child
						LEFT JOIN _top_sentences top_s ON top_s.sentence = tr.sentence
				),
				s (child, match) AS (
					SELECT ts.r_cid, top_s.sentence FROM test.rsentence ts
						LEFT JOIN _top_sentences top_s ON top_s.sentence = ts.sentence
						WHERE ts.sentence = %s
					UNION
					SELECT tt.parent, top_s.sentence FROM s
						INNER JOIN test.rtree tt ON tt.child = s.child
						INNER JOIN test.rsentence tr ON tr.r_cid = tt.parent
						LEFT JOIN _top_sentences top_s ON top_s.sentence = tr.sentence
				)
				SELECT ts.body FROM (
					SELECT parent AS id FROM r WHERE match IS NOT NULL
						UNION
					SELECT child AS id FROM s WHERE match IS NOT NULL
				) st1
					INNER JOIN test.rsentence ts ON ts.r_cid = st1.id;
			''', (W[i][0], W[i][0]))
			matches = cur.fetchall()
			cur.execute('SELECT body FROM test.rsentence WHERE sentence = %s', (W[i][0],))
			original = cur.fetchall()
			if len(matches) > 0:
				print(matches, original, top_rows)
			conn.rollback()
		# see top 5 max matches branch
		# for i, (sid_l, left) in enumerate(D_items):
		# 	for sid_r, right in D_items[i:]:
		# 		K.model.similarity(left, right)
		
if __name__ == '__main__':
	run()