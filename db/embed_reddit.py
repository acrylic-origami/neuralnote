import sys
import tensorflow as tf
import tensorflow_hub as hub
import psycopg2
import psycopg2.extras
from functools import reduce

def run():
	with tf.Graph().as_default(), psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
		embed = hub.Module('/home/d/nl/sentence-embed')
		
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute('SELECT sentence, body FROM test.rsentence LIMIT 10000;')
		sentences = cur.fetchall()
		embeddings = embed([s['body'] for s in sentences])
		
		with tf.Session() as sess:
			sess.run(tf.global_variables_initializer())
			sess.run(tf.tables_initializer())
			for i, embedding in enumerate(sess.run(embeddings)):
				sys.stdout.write('\r%d' % i)
				cur.execute('INSERT INTO sentence_embed (i, embed, sentence) VALUES %s' % ('(%s,%s,%s),' * embedding.shape[0])[:-1], reduce(lambda acc, a: acc + a + (sentences[i]['sentence'],), enumerate(embedding.tolist()), tuple()))
				conn.commit()

if __name__ == '__main__':
	run()