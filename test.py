import nltk

##Datasets download on first run
#nltk.download('averaged_perceptron_tagger') #for tagger
#nltk.download('punkt') #for tokenize

blob = "I feel that eggs are the best breakfast food due to their high protein content. He wanted food too."

tokens = nltk.word_tokenize(blob)
print(tokens)

tagged = nltk.pos_tag(tokens)
print(tagged)

for word in tagged:
	print(word[0] +" "+  word[1])
