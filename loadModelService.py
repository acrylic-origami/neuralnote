#https://stackoverflow.com/questions/42986405/how-to-speed-up-gensim-word2vec-model-load-time/43067907

from gensim.models import KeyedVectors
from threading import Semaphore
model = KeyedVectors.load('/home/data/word2vec_models/glove.6B.300d.model', mmap='r')
model.syn0norm = model.syn0  # prevent recalc of normed vectors
model.most_similar('stuff')  # any word will do: just to page all in
Semaphore(0).acquire()  # just hang until process killed