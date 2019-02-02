#https://stackoverflow.com/questions/42986405/how-to-speed-up-gensim-word2vec-model-load-time/43067907
from gensim.models import KeyedVectors
from threading import Semaphore

#Load Model
model = KeyedVectors.load('/home/data/word2vec_models/glove.6B.300d.model', mmap='r')
model.syn0norm = model.syn0  # prevent recalc of normed vectors

#Use Model
print(model.most_similar('stuff'))
print(model.similarity("eggs", "egg"))
vector = []
vector.append(model["elder"])
print(vector)


#THIS FUNCTION DOES NOTHING YET - JUST TESTING CODE