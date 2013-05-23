import sys, pickle, nltk, ner
from nltk.tree import Tree

tagged_words = None
tagged_sentences = None
people = None
sentences = None

# A bunch of utils to make the life easier

def join_tagged(tagged):
	s = ""
	for text, tag in tagged:
		s += " "+text+"/"+tag
	return s
	
# extracts features from text - here the features are the words themselves
def bag_of_words(tokens, text, stemmer):
	bag = {}
	for t in tokens:
		t_lower = t.lower()
		if len(t) > 1:
			bag[stemmer.lemmatize(t_lower)] = True
			''' disabled features, as they just lower the accuracy of the classifier
			bag['starts with %c'%t_lower[0]] = True
			bag['ends with %c'%t_lower[-1]] = True
			pos = text.index(t)
			if pos > 0:
			bag['%s after %s'%(t_lower, text[pos-1].lower())] = True
			if pos+1 < len(text):
			bag['%s after %s'%(text[pos+1].lower(), t_lower)] = True
			if pos > 0 and pos+1 < len(text):
			bag['3gram(%s %s %s)'%(text[pos-1].lower(), t_lower, text[pos+1].lower())] = True'''
	return bag
	
def get_names_dict(people):
	names = {}
	for i, (fullname, data) in enumerate(people.items()):
		for shortname in data['shortnames']:
			for s in shortname.lower().split(" "):
				names[s] = data
			names[shortname.lower()] = data
		for shortname in fullname.lower().split(" "):
			names[shortname] = data
		names[fullname.lower()] = data
	return names
	
def _depth_retag(what, node_tag, bag):
	if type(what) == Tree:
		for leaf in what:
			_depth_retag(leaf, what.node, bag)
	else:
		bag.append((what[0],what[1],node_tag))
	
def retag_chunked(chunked_sentence):
	retaged = []
	_depth_retag(chunked_sentence, None, retaged)
	return retaged
		
def load_data(article_text):
	global tagged_words, tagged_sentences, people, sentences
	# we give parameter to load everything from file and to save some time :) 
	if "-f" in sys.argv:
	  # tokenize & tag all words in article
	  print "Tokenizing & tagging words..."
	  tokens = nltk.tokenize.wordpunct_tokenize(article_text)
	  tagged_words = nltk.pos_tag(tokens)
	  pickle.dump(tagged_words, file('tagged_words.pickle', 'w'))

	  # extract & tokenize each sentence separately
	  print "Tokenizing & tagging sentences..."
	  sentences = nltk.tokenize.sent_tokenize(article_text)
	  pickle.dump(sentences, file('sentences.pickle', 'w'))
	  
	  tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences]
	  tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]
	  pickle.dump(tagged_sentences, file('tagged_sentences.pickle', 'w'))
	  
	  print "Searching for people..."
	  instance  = ner.NERFinder()
	  people = instance.find(tagged_words, sentences, tagged_sentences)
	  pickle.dump(people, file('people.pickle', 'w'))
	else:
	  tagged_sentences =  pickle.load(file('tagged_sentences.pickle', 'r'))
	  tagged_words =  pickle.load(file('tagged_words.pickle', 'r'))
	  sentences =  pickle.load(file('sentences.pickle', 'r'))
	  people =  pickle.load(file('people.pickle', 'r'))