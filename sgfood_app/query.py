import requests
from .clean_data import clean_review
import re, string
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
import time

#TYPES OF QUERIES HANDLES
#1. question kind(find the food only, is the __ in __ good
#2. food of a rest (top 10 reviews about the food)
#3. food only (restaurants and child docs with the food, top 2 per rest)
#4. restaurant only (latest)

def bigram(phrase):
	""" Used for determining if restaurant name is in query string """
	phrase=re.compile('[%s]' % re.escape(string.punctuation)).sub('',phrase).lower()
	tokens=phrase.split(" ")
	bigram_list=[]
	#bigram_list.append(tokens[0])
	print(bigram_list)
	if len(tokens)>1:
		for i in range(len(tokens)-1):
			bigram_list.append(tokens[i]+" "+tokens[i+1])

	return bigram_list+[w for w in tokens if not w in stop_words]

def query_index(query_url):
	""" Query index given formatted query to API """
	print(query_url)
	r = requests.get(query_url)
	r.raise_for_status()
	json_data = r.json() #dict type
	print("QUESTY INDEX")
	if len(json_data["response"]["docs"])>0:

		for rest in json_data["response"]["docs"]:

			if "_childDocuments_" in rest:
				print("underscore!")
				rest["childDocuments"]=rest["_childDocuments_"]
				del rest["_childDocuments_"]
		return json_data
	else:
		return "no results"

def query_review_body(query): #review body only
	#where to find <food>
	""" to query reviews: Clean query and generate query string to post to API"""
	query="\"AND\"".join(clean_review(query))
	query_url= "http://127.0.0.1:8983/solr/food/query?q={!parent%20which=path:1.restaurants%20AND%20score=total}path:2.restaurants.reviews%20AND%20review_body:(\""+query+"\")&fl=*,[child%20parentFilter=path:1.restaurants%20childFilter=review_body:(\""+query+"\") limit=10]&sort=score%20desc"

	return query_index(query_url)

def query_rest_name(rest_list): #rest name only
	""" to query rest name: Clean query and generate query string to post to API"""
	rest_string=" OR ".join([rest for rest in rest_list])
	query_url="http://127.0.0.1:8983/solr/food/query?q=path:1.restaurants%20AND\
	%20rest_name:(\""+rest_string+"\")&fl=*,[child%20parentFilter=path:1.restaurants]"

	return query_index(query_url)

def query_rest_name_and_review_body(rest_list, query):
	""" to query reviews and restname: Clean query and generate query string to post to API"""
	rest_name_query_substring = " OR ".join([rest_name.lower() for rest_name in rest_list])
	
	print(clean_review(query.lower().replace(rest_list[0].lower(), "")))
	query=query.lower().replace(rest_list[0].lower(), "")
	cleaned_query=clean_review(query)
	query_substring=" ".join(clean_review(query.lower().replace(rest_list[0].lower(), "")))
	print(rest_name_query_substring)
	query_url= "http://127.0.0.1:8983/solr/food/query?q={!parent%20which=\"path:1.restaurants%20AND%20rest_name:("+rest_name_query_substring+")\"%20AND%20score=total}path:2.restaurants.reviews%20AND%20review_body:"+query_substring+"&fl=*,[child%20parentFilter=path:1.restaurants%20childFilter=review_body:"+query_substring+"]&sort=score%20desc"

	return query_index(query_url)

def check_question(query): #decide if query food and remove question words
	""" simple check to see if query is a question and re-query """
	question_words = ['where','to','find', 'eat','?', 'how', 'what', 'which']
	querywords = query.split()
	check_question=[word for word in querywords if word.lower() in question_words]
	if check_question: #if list is not empty
		 #words that TFIDF cannot capture
		querywords  = [word for word in querywords if word.lower() not in question_words]
		processed_query = ' '.join(querywords)
		print(processed_query)
		return 1, processed_query

	return 0, query



def check_if_rest_names(query): #decide if rest_name in query
	""" full restaurant name is in the query """
	print("checkifrestname")
	bigrams = bigram(query.lower())
	print(" OR ".join(bigrams))
	query_url="http://127.0.0.1:8983/solr/food/query?q=rest_name:("+" OR ".join(bigrams)+")"
	result=query_index(query_url)

	if result != "no results":
		restaurants=result["response"]["docs"]
		for rest in restaurants:
			print(rest["rest_name"])
		rest_list=[]
		print(restaurants)
		for restaurant in restaurants:
			#print(restaurant["rest_name"])
			#print(restaurant["rest_name"][0].lower())
			#print(query.lower())
			#print(restaurant["rest_name"][0].lower())
			#print(rest_list)
			if restaurant["rest_name"][0].lower() in query.lower():

				rest_list.append(restaurant["rest_name"][0])
				query_remaining=query.lower().replace(rest_list[0].lower(),"")
				print("BEF:"+ query_remaining)
				query_remaining = " ".join([w for w in query_remaining.split() if not w in stop_words])
				print("AFT:" + query_remaining)
		if rest_list:
			return 1, rest_list, query_remaining
		else:
			return 0, [], query
	else: #none found
		return 0, [], query



def query_solr(query):
	""" Given query returns Json Data as dict """
	#time how long querying the index takes
	start=time.time()
	#check if rest_name in query
	rest_result_code, rest_list, query_remaining= check_if_rest_names(query) #1 for rest, 0 for none
	#check if question, remove question terms
	#print(rest_result_code, rest_list, query_remaining)
	qns_result_code, processed_query = check_question(query_remaining) #c0 for no, 1 for yes
	#print(processed_query)
	if (rest_result_code ==1):
		#if got food in query: query both
		if (processed_query):
			#print(processed_query)
			#print(rest_list)
			json_data=query_rest_name_and_review_body(rest_list, processed_query)
		else:
			json_data=query_rest_name(rest_list)

		end=time.time()
		print("time elapse: ****{}".format(str(end-start)))
		return json_data
	if (rest_result_code==0):
		#query review body only
		print(processed_query)
		json_data=query_review_body(processed_query)
		end=time.time()
		print("time elapse: ****{}".format(str(end-start)))
		return json_data

