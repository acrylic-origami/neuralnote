import nltk

entity_tokens = ["NN", "NNS", "NNP", "NNPS", "PRP", "PRP$", "SYM"]

#This function generates the entities from a sentence 
def parseSentence(data):

	#Tokenize sent.
	tokens = nltk.word_tokenize(data)

	#Tag sent.
	tagged = nltk.pos_tag(tokens)

	##Generate entities
	entities = []

	#Singular entities 
	i=0
	for word in tagged:
		if word[1] in entity_tokens:
			entities.append([word[0], word[1], i]) #we create (WORD, POS, SENT_INDEX), SENT_INDEX 0 aligned

		i = i + 1

	#Series entities 
	i = 0
	while i < len(tagged):
		
		if tagged[i][1] in entity_tokens:
			length = 1

			j = i + 1
			candidate_phrase = [tagged[i][0]] #add first word to set
			candidate_phrase_tokens = [tagged[i][1]] #add tags
			while j < len(tagged) and tagged[j][1] in entity_tokens:
				candidate_phrase.append(tagged[j][0])
				candidate_phrase_tokens.append(tagged[j][1])
				j = j + 1

			#If we have a run 
			if len(candidate_phrase) > 1:
				entities.append([' '.join(candidate_phrase), ' '.join(candidate_phrase_tokens), i])
				i = j


		i = i + 1

	return entities


print(parseSentence("I feel that eggs are the best breakfast food table due to their high protein content."))