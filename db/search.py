import json
import sys
import psycopg2
import psycopg2.extras
import re
from functools import reduce

import tensorflow as tf
import tensorflow_hub as hub

# from embed import sess, embed

if __name__ == '__main__':
	def run():
		with tf.Graph().as_default():
			with tf.Session() as sess:
				embed = hub.Module('/home/d/nl/sentence-embed')
				sess.run(tf.global_variables_initializer())
				sess.run(tf.tables_initializer())
				with psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
					cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					
					# J = json.loads(sys.stdin.readlines())
					
					while True:
						R = 'I attended QHacks and I lost.' # sys.stdin.readlines().split(['.', '\n'])
						# print('Processing...')
						L = sess.run(embed([s for s in re.split(r'[\.\n]', R) if s != '']))
						for l in L:
							cur.execute('CREATE TEMPORARY TABLE embed_ (i INT, embed FLOAT) ON COMMIT DROP;')
							cur.execute('INSERT INTO embed_ (i, embed) VALUES %s' % ('(%s, %s),' * l.shape[0])[:-1], reduce(lambda acc, a: acc + a, enumerate(l.tolist()), tuple()))
							cur.execute('''SELECT DISTINCT ON (st0.s, ts.body), st0.sentence FROM (SELECT SUM(POWER(se2.embed - se.embed, 2)) AS s, se2.sentence FROM embed_ se INNER JOIN sentence_embed se2 ON se.i = se2.i GROUP BY se2.sentence) st0 INNER JOIN test.rsentence ts ON ts.sentence = st0.sentence GROUP BY st0.sentence ORDER BY s ASC LIMIT 10;''')
							print("\n\n".join([ k['body'] for k in cur.fetchall() ]))
							cur.rollback()
						
	run()