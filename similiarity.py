import pandas as pd 
import numpy as np 
from structures import *
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize 

def parse_ep(eps):
	d = {}
	for line in eps:
		if line.startswith("Season"):
			continue
		elif line.startswith("S"):
			e = Episode(line[line.find(" "):line.find("(")].strip(), 
						rate=line[1+line.find("("):line.rfind("/")].strip(),
						code=line[:line.find(".")].strip())
			e.description = eps.readline().strip()
			d[e] = e.description
	return d

def remove_punc(word):
	PUNC = [",", ".", "'",'"', ";"]
	for c in word:
		if c in PUNC:
			word = word[:word.find(c)]
			break
	return word

def clean_sentence(sentence):
	_filter = set(stopwords.words('english'))
	_filter.add("the")
	_filter.add("")
	_filter.add("and")
	filtered = []
	for word in sentence.split():
		if not word.lower() in _filter:
			word = word.lower()
			word = remove_punc(word)
			filtered += [word]
	return filtered

def clean_dict(d):
	for ep in d:
		d[ep] = clean_sentence(d[ep])
		d[ep] += ep.title.lower().split()
	return d

def bag_of_words(sentence):
	bag = {}
	for word in sentence:
		if bag:
			for key in bag:
				if key in wn.synset(word):
					bag[word] = bag.get(word, 0) + 1
		else:
			bag[word] = bag.get(word, 0) + 1
	return bag

def jaccard(u, v):
	a = set(u)
	b = set(v)
	c = a.intersection(b)
	return float(len(c)) / (len(a) + len(b) - len(c))

def compute_tf(t, D):
	tf_dict = {}
	n = len(t)
	for k, v in D.items():
		tf_dict[k] = v/n
	return tf_dict

def compute_idf(corpus):
	import math
	idf_dict = {}
	N = len(corpus)

	idf_dict = dict.fromkeys(corpus[0].keys(), 0)
	for dct in corpus:
		for word, freq in dct.items():
			if freq > 0:
				idf_dict[word] += 1

	for word, freq in idf_dict.items():
		idf_dict[word] = math.log10(N/freq)
	return idf_dict

def tf_idf(tf_dict, idf_dict):
	tfidf = {}
	for word, freq in tf_dict.items():
		tfidf[word] = freq*idf_dict[word]
	return tfidf

def compute_tfidf(corpus):
	v = [x.split() for x in corpus]
	s = set()
	for lst in v:
		s = s.union(set(lst))
	dct_lst = []
	tf_dicts = []
	for text in corpus:
		dct = dict.fromkeys(s, 0)
		line = text.split()
		for word in line:
			dct[word] += 1
		dct_lst += [dct]
		tf_dict = compute_tf(line, dct)
		tf_dicts += [tf_dict]
	idf_dict = compute_idf(dct_lst)
	tfidf_dicts = []
	for tf in tf_dicts:
		tfidf = tf_idf(tf, idf_dict)
		tfidf_dicts += [tfidf]
	return tfidf_dicts
	
def cosine_sim(u, v):
	nu = np.linalg.norm(u)
	nv = np.linalg.norm(v)
	dot_prod = np.dot(np.array(u), np.array(v))
	return dot_prod / (nu*nv)