#word2vec implementation:

import pandas as pd
import numpy as np
from nltk.tag import pos_tag_sents
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
import nltk
import os, re
np.random.seed(0)
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
file_list=[]
files=os.listdir()



for f in files:
	if f[-4:]=='.txt':
		file_list.append(f[:-4])


def read_textfile(f): #conv textfile to dataframe
	filename="{}.txt".format(f)
	with open(filename) as f:
		content = f.readlines()
		content = [x.strip() for x in content]
	return content

def load_ratings_and_reviews(text_contents):
	ratings=[]
	reviews=[]
	i=0
	while i<(len(text_contents)):
		if len(text_contents[i])==1:#assuming review is len==1
			ratings.append(text_contents[i])
			i+=1
			reviews.append(text_contents[i])
			i+=1
		else:#join review w previous review
			#ratings.append("0")
			#print(i)
			print("hi")
			#reviews.append(text_contents[i])
			last_review_position=len(reviews)-1
			reviews[last_review_position]=reviews[last_review_position]+text_contents[i]
			i+=1
	return ratings, reviews

def make_dataframe(ratings, reviews):
	#df=pd.DataFrame(columns=['ratings','reviews'])
	df=[]
	print(len(ratings))
	print(len(reviews))
	for r in range(len(ratings)):
		df.append({"score": ratings[r], "Review": reviews[r]})
	df=pd.DataFrame(df)
	print(df.head())
	return df
#for review in reviews:
#	tokens=word_tokenize(review)
#	print(tokens)

#break into sentences and find out words tha


def get_all_reviews(df):
	row_count=len(df)
	list_service_reviews=[]
	print(row_count)
	for i in range(row_count):
		if ("service" in df['Review'].iloc[i]):
			review_tokenized=sent_tokenize(df['Review'].iloc[i])
			for s in range(len(review_tokenized)):
				if "service" in review_tokenized[s]:
					list_service_reviews.append(review_tokenized[s])
					try:
						list_service_reviews.append(review_tokenized[s+1])
					except IndexError as err:
						print("INDEX: it's the last")
	return list_service_reviews

def sentence_to_wordlist(sentence, remove_stopwords=False):
    # 1. Remove non-letters
    sentence_text = re.sub(r'[^\w\s]','', sentence)
    # 2. Convert words to lower case and split them
    words = sentence_text.lower().split()
    # 3. Return a list of words
    return(words)


def oped_to_sentences(oped, tokenizer, remove_stopwords=False ):

        # 1. Use the NLTK tokenizer to split the text into sentences
    raw_sentences = tokenizer.tokenize(oped.strip())
    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call sentence_to_wordlist to get a list of words
            sentences.append(sentence_to_wordlist(raw_sentence))
    # 3. Return the list of sentences (each sentence is a list of words, so this returns a list of lists)
    len(sentences)
    return sentences


contents=[] # list of sentences

for rest in file_list:
	contents=contents+read_textfile(rest)
ratings, reviews=load_ratings_and_reviews(contents)
df=make_dataframe(ratings, reviews) #df of all scores and reviews

nyt_opeds = df['Review'].tolist()

sentences = []

for i in range(0,len(nyt_opeds)):

    # Need to first change "./." to "." so that sentences parse correctly
    #oped = nyt_opeds[i].replace("/.", '')
    # Now apply functions
    sentences += oped_to_sentences(nyt_opeds[i], tokenizer)


print("There are " + str(len(sentences)) + " sentences in our corpus of opeds.")
print(sentences[220])

import gensim
from gensim.models import Word2Vec
from gensim.models import word2vec
from gensim.models import Phrases
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

num_features = 300    # Word vector dimensionality                      
min_word_count = 50   # Minimum word count                        
num_workers = 4       # Number of threads to run in parallel
context = 6           # Context window size                                                                                    
downsampling = 1e-3   # Downsample setting for frequent words

model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)
model.init_sims(replace=True)

model_name = "nytimes_oped"
model.save(model_name)
new_model = gensim.models.Word2Vec.load('nytimes_oped')
vocab = list(model.wv.vocab.keys())
print(vocab[:25])

print(model.most_similar('service',  topn=50))