import nltk, data, summarize, pickle, ner, config, training, sys, utils
from nltk.tree import Tree

# show commandline arguments
print "CLI:", sys.argv

path = "db/ivonyte-aiste/2011-7-3-1.txt"
article = data.Article(path)
print "-"*80
print article.text
print "-"*80

# we give parameter to load everything from file and to save some time :) 
if "-f" in sys.argv:
  # tokenize & tag all words in article
  print "Tokenizing & tagging words..."
  tokens = nltk.tokenize.wordpunct_tokenize(article.text)
  tagged_words = nltk.pos_tag(tokens)
  pickle.dump(tagged_words, file('tagged_words.txt', 'w'))

# extract & tokenize each sentence separately
  print "Tokenizing & tagging sentences..."
  sentences = nltk.tokenize.sent_tokenize(article.text)
  pickle.dump(sentences, file('sentences.txt', 'w'))
  tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences]
  tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]
  pickle.dump(tagged_sentences, file('tagged_sentences.txt', 'w'))
else:
  tagged_sentences =  pickle.load(file('tagged_sentences.txt', 'r'))
  tagged_words =  pickle.load(file('tagged_words.txt', 'r'))
  sentences =  pickle.load(file('sentences.txt', 'r'))

# show the output
print utils.join_tagged(tagged_words)
print "-"*80
print tagged_sentences
print "-"*80

# WDT - with, CD - number, CC - and, PRP - she;I, POS - `, MD - will, PRP$ - his, JJ - crucial;political, RB - even, not
# IN - at/in, DT - a, the, those, NN - noun(sun, dog, ...)
# TODO: revise grammar & regexp
grammar = r"""
  APLINKYBES: {<IN><DT|CD|NN.*|POS|:>+<IN>*}
  VIETA: {<NNP><NN..>+}
  VEIKSNYS: {<DT><JJ>*<NN.*>*<:>*<NN.>*} # Chunk sequences of DT, JJ, NN
  TARINYS: {<EX>*<MD>*<RB>?<V.|V..>+<IN>*<NP|PP>*<TO>?<RB>?<JJ|NN>?<V.|V..>*} # Chunk verbs and their arguments
  OBJEKTAS: {<NN.>*<:|C.>*<NN.>*}
  PAPILDINYS: {<RB>*<IN>*<DT>*<JJ>*<NN?>*}
  JUNGTUKAS: {<CC>}
  IVARDIS: {<PRP.*><PRP.*>*}
  """

''' old backup grammar:
grammar = r"""
  APLINKYBES: {<IN><DT|CD|NN.*|POS|:>+}
  VIETA: {<NNP><NN..>+}
  VEIKSNYS: {<DT><JJ>*<NN.*>+}        # Chunk sequences of DT, JJ, NN
  TARINYS: {<MD>*<V.|V..>*<IN*><NP|PP>*<TO>?} # Chunk verbs and their arguments
  PAPILDINYS: {<IN>*<DT>*<JJ><NN?>*}
  SAKINYS: {<APLINKYBES><VEIKSNYS><TARINYS><APLINKYBES>*}
  BRAND: {<NN.>*<:|CD>*<NN.>*}
  """
'''

# do our custom chunking
cp = nltk.RegexpParser(grammar) 

instance  = ner.NERFinder()
people = instance.find(tagged_words, sentences, tagged_sentences)

start = 0
end = 15
for index, sentence in enumerate(tagged_sentences):
	chunked_sentence = cp.parse(sentence) # nltk.chunk.ne_chunk(sentence)


	if (index < end and index >= start):
		print "oooo", sentences[index]
		print
		print "####", chunked_sentence
	