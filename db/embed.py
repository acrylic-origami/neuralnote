import sys
import tensorflow as tf
import tensorflow_hub as hub
import psycopg2
import psycopg2.extras
import json
from functools import reduce

with tf.Graph().as_default():
	with tf.Session() as sess:
		embed = hub.Module('/home/d/nl/sentence-embed')
		sess.run(tf.global_variables_initializer())
		sess.run(tf.tables_initializer())
		
		def run():
			with psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
				J = json.loads("".join(sys.stdin.readlines()))
				embedding = sess.run(embed(J['body']))
				
				cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				cur.execute('INSERT INTO sentence_embed (i, embed, sentence) VALUES %s' % ('(%s,%s,%s),' * embedding.shape[0])[:-1], reduce(lambda acc, a: acc + a + (J['id']), enumerate(embedding.tolist()), tuple()))
				conn.commit()
				# cur.execute('SELECT sentence, body FROM test.rsentence LIMIT 10;')
				# sentences = cur.fetchall()

		if __name__ == '__main__':
			run()