import pandas as pd
import numpy as np
from nltk.tag import pos_tag_sents
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
np.random.seed(0)

import os
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
	"""
	df=pd.DataFrame()
	#check if score and review really alternates
	#check for NaN values
	line=0
	for i in range(celen(content)/2):
		score=content[0]
		review=content[i+1]
		df.append({"score": score, "review": review}, ignore_index=True )
		line+=2
	print(df.head())
	"""

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

def get_1_stars_service(df): #return list of reviews
	#process into sentences????
	row_count=len(df)
	list_service_reviews=[]
	print(row_count)
	for i in range(row_count):
		if (df['score'].iloc[i]=="1") and ("service" in df['Review'].iloc[i]):
			review_tokenized=sent_tokenize(df['Review'].iloc[i])
			for s in range(len(review_tokenized)):
				if "service" in review_tokenized[s]:
					list_service_reviews.append(review_tokenized[s])
	return list_service_reviews

def get_5_stars_service(df):
	row_count=len(df)
	print(row_count)
	for i in range(row_count):
		if (df['score'].iloc[i]=="5"):
			print(df['Review'].iloc[i])
	return

def get_all_reviews(df):
	row_count=len(df)
	list_service_reviews=[]
	print(row_count)
	for i in range(row_count):
		if ("service" in df['Review'].iloc[i]) or ("Service" in df['Review'].iloc[i]):
			review_tokenized=sent_tokenize(df['Review'].iloc[i])
			for s in range(len(review_tokenized)):
				if "service" in review_tokenized[s] or "Service" in review_tokenized[s]:
					list_service_reviews.append(review_tokenized[s])

	return list_service_reviews
def process_those_sentences(list_service_reviews): #find top 10 common words
	bag_of_tokens=[]
	for sentence in list_service_reviews:
		#tokens=word_tokenize(sentence)
		tokenizer = RegexpTokenizer(r'\w+')
		tokens=tokenizer.tokenize(sentence)
		filtered_words = [token for token in tokens if token not in stopwords.words('english')]
		for filtered_word in filtered_words:
			bag_of_tokens.append(filtered_word)

	fdist = FreqDist(bag_of_tokens)
	top_50=fdist.most_common(1000)

	return top_50

contents=[]

for rest in file_list:
	contents=contents+read_textfile(rest)
ratings, reviews=load_ratings_and_reviews(contents)
df=make_dataframe(ratings, reviews)
list_service_reviews=get_all_reviews(df)
top_200=process_those_sentences(list_service_reviews)

top_200=[word[0] for word in top_200]
pos=pos_tag(top_200)
pronoun_list = ['PRP', 'IN', 'RB', 'JJ']
ok=[s for s in pos if s[1] not in pronoun_list]
print([p for p in ok])

#get sentences with service and find most common words with it???
#tokenize and clean those sentences and find the most common words?

