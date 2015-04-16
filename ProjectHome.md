## About ##
http://code.google.com/p/py-nltk-dev/
```
This code is a research/academic project conducted at Kaunas University of Technology (Lithuania) in 2013-05 
by two Informatics faculty MSc students: Aiste Ivonyte & Tomas Uktveris.

Project analyses & applies natural language processing(NLP) algorithms 
to texts extracted from certain year Wikipedia archived news articles.
```

The created text analyzer does the following (for a given article):

  1. **Extracts named entities** (people) - the named entity recognition (NER) problem [ner.py]<br>  (uses default Python NLTK ne_chunker + extra logic to detect sex/city/country & remove false positives)<br />
<ol><li><b>Creates a summary from article text</b> [summarize.py, ph_reduction.py]<br>Two methods used:<br>
<ul><li>Sentences with most frequent words - Summary I<br>
</li><li>Phrase reduction method - Summary II<br />
</li></ul></li><li><b>Classifies the article into 5 most frequent (top) categories from all analyzed Wikipedia articles</b> [training.py, training_binary.py]<br>Uses three  NLTK library built-in classifiers - Bayes, MaxEnt (regression) and DecisionTree.<br>Two approaches are used for classifier training:<br>
<ul><li>Multiclass - classifier is trained to detect 1 class from multiple (7 classes in total)<br>
</li><li>Binary - trains 3x6 binary classifiers to detect if article represents a given category<br />
</li></ul></li><li><b>Finds people actions</b> [action.py]<br>Custom token & sentence analysis - reuses NER data to find & assign references.<br />
</li><li><b>Resolves references/anaphoras</b> (named entity normalization - NEN) [references.py]<br>Custom token & sentence analysis - reuses NER data to find required verbs.<br />
</li><li><b>Finds people interactions</b> [interactions.py] <br> Custom token & sentence analysis - reuses NER & reference data for finding multiple people in sentence and their actions.</li></ol>

<h2>License</h2>
Code & project provided under MIT license (<a href='http://opensource.org/licenses/mit-license.php'>http://opensource.org/licenses/mit-license.php</a>). <br>Use at your own risk, no guaranties or warranty included.<br>
<br>
Female/male names dictionary used from NLTK project: <a href='https://code.google.com/p/nltk/'>https://code.google.com/p/nltk/</a><br>
English words dictionary used from: <a href='http://www-01.sil.org/linguistics/wordlists/english/'>http://www-01.sil.org/linguistics/wordlists/english/</a><br>
World cities database used from: <a href='http://www.maxmind.com/en/worldcities'>http://www.maxmind.com/en/worldcities</a>

<h2>Requirements</h2>
<ul><li>Python 2.7 (<a href='http://www.python.org/download/releases/'>http://www.python.org/download/releases/</a>)<br>
</li><li>Python NLTK library (<a href='http://nltk.org/'>http://nltk.org/</a>) + installed all available corporas (>>> import nltk; nltk.download())</li></ul>

<h2>Directory structure</h2>
<ul><li><b>.</b> - (root directory) contains all source code for the analyzer<br>
</li><li><b>./archives</b> - contains EN generic word, people names & country dictionaries, SQL city names DB files & scripts<br>
</li><li><b>./db</b> - contains extracted Wikipedia articles by month<br>
</li><li><b>./FtpDownloader</b> - Java utility to download articles DB from FTP site<br>
</li><li><b>./other</b> - misc & example scripts</li></ul>

<h2>Usage</h2>
<b>Running the analyzer</b>
<hr />
<ol><li>Run article parser & data generation utility to generate the required data files for the next step:<pre><code> &gt;&gt; python data.py </code></pre>
</li><li>Run multiclass trainer to generate three types of classifier files:<br>
<pre><code>  &gt;&gt; python training.py -b <br>
  &gt;&gt; python training.py -m<br>
  &gt;&gt; python training.py -d<br>
</code></pre>
</li><li>Run binary trainer to generate other classifier files:<br>
<pre><code>  &gt;&gt; python training_binary.py -b<br>
  &gt;&gt; python training_binary.py -m<br>
  &gt;&gt; python training_binary.py -d <br>
</code></pre>
</li><li>Run the main analyzer script to analyze a given article:<br>
<pre><code>  &gt;&gt; python main.py -f db/klementavicius-rimvydas/2011-12-03-1.txt<br>
</code></pre></li></ol>

<b>Running other tests</b>
<hr />
<blockquote>Some analyzer functionality can be tested separately by running the test_xxxx.py files.</blockquote>
