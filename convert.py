from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

glove_file = datapath('/home/data/glove_models/glove.6B.300d.txt')
tmp_file = get_tmpfile("/home/data/word2vec_models/glove.6B.300d.txt")

_ = glove2word2vec(glove_file, tmp_file)