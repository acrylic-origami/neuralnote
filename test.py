from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec


file = datapath("/home/data/word2vec_models/glove.6B.300d.txt")
model = KeyedVectors.load_word2vec_format(file, binary=False)

model.init_sims(replace=True)
print(model.similarity("nick", "derek"))