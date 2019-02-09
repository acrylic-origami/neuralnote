import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import scipy.spatial.distance


with tf.Graph().as_default():
	embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")
	embeddings = embed([
	"I go to the university of western ontario and study computer science.", "I go to the university of western ontario and study computer science."])

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
		sess.run(tf.tables_initializer())

		output = sess.run(embeddings)

		distance = scipy.spatial.distance.cosine(output[0],output[1])

		print(distance)
