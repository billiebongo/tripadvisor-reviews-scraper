import django
import os
import json
import requests
from .lib.file_handler import (find_files_in_dir, get_ratings_reviews_from_textfile, get_burple_reviews)
from .lib.find_mrt import find_mrt
from .models import Restaurant, Review
import random
import re
"""
Upload reviews and rest and labels into DB

"""

API_KEY="AIzaSyAfxgeYfRVqGS6bcCtnCc5X5ch9ekK4EIc"

DATA_DIR='sgfood_app/data/TA/'




def calcScore(ratings):
	total_score=0
	for r in range(len(ratings)):
		try:
			total_score+= int(ratings[r])
		except ValueError:
			total_score+= 0
	total_score=total_score/len(ratings)
	if total_score==0:
		print("ERROR: total score is 0")
	return total_score

def create_review(restaurant, score, review_body):
	review=Review.objects.create(restaurant=restaurant, review_body=review_body, score=score)
	return review

def create_burpple_review(restaurant, review_body):
	review=Review.objects.create(restaurant=restaurant, review_body=review_body)
	return review

def get_url(filename):

	with open('sgfood_app/url_list.txt') as f:
		for line in f:

			if "Reviews-"+filename in line:
				return "https://www.tripadvisor.com.sg"+line
	print("not found")
	return None

def get_burpple_url(filename):
	with open('sgfood_app/burple_url.txt') as f:
		for line in f:
			if filename in line:

				return "https://www.burpple.com/" + line
	print("not found")
	return None



def get_attributes(filename):
	
	with open('sgfood_app/data/labels/labels.json') as js:
		labels_dict=json.load(js)
		try:
			attr=labels_dict[filename]
			if attr["price"]=="NULL":
				p=-1
			else:
				p=int(attr["price"])/10
			if attr["f"]=="NULL":
				f=-1
			else:
				f=int(attr["f"])/10
			if attr["s"]=="NULL":
				s=-1
			else:
				s=int(attr["s"])/10
			if attr["v"]=="NULL":
				v=-1
			else:
				v=int(attr["v"])/10				
			if attr["a"]=="NULL":
				a=-1
			else:
				a=int(attr["a"])/10
			return {"price": p, "a": a, "v":v, "f": f, "s": s}
		except:
			return {"price": -1, "a": -1, "v": -1, "f": -1, "s": -1}


def create_restaurant(filename, rest_name, ratings, reviews ):
	with open(DATA_DIR+filename+'.txt') as f:
		total_score=calcScore(ratings)
	rest_name=filename.replace("_", " ")
	print(filename)
	url = get_url(filename)
	attr=get_attributes(filename)
	restaurant=Restaurant.objects.create(rest_name=rest_name, url=url, total_score=total_score,\
	price=attr['price'],food_score=attr['f'], service_score=attr['s'], value_score=attr['v'],ambience_score=attr['a'])
	for i in range(len(reviews)):
		review=create_review(restaurant, ratings[i], reviews[i])
		restaurant.reviews.add(review)

		restaurant.save()

def create_burpple_restaurant(filename, reviews):
	rest_name=filename.replace("_", " ")
	url=get_burpple_url(filename)
	print(url)
	restaurant=Restaurant.objects.create(rest_name=rest_name, url=url)
	for i in range(len(reviews)):
		review=create_burpple_review(restaurant, reviews[i])
		restaurant.reviews.add(review)

		restaurant.save()


def change_rest_name():
	restaurants=Restaurant.objects.filter(id__gte=3756)
	for restaurant in restaurants:
		restaurant.rest_name=restaurant.rest_name.replace("-", " ")
		print(restaurant.rest_name)
		restaurant.save()


def run_script():
	"""
	get all textfiles in dir and create each rest and their reviews
	"""
	file_list=find_files_in_dir()

	
	for i in range(len(file_list)):
		print(file_list[i])
		rest_name=file_list[i]
		ratings, reviews = get_ratings_reviews_from_textfile(file_list[i])
		create_restaurant(file_list[i], rest_name, ratings, reviews)


def burpple_db_start():
	file_list=find_files_in_dir()

	
	for i in range(len(file_list)):
		print(file_list[i])
		rest_name=file_list[i]
		
		contents=get_burple_reviews(file_list[i])
		#create_restaurant(file_list[i], rest_name, ratings, reviews)
		print(file_list[i])
		create_burpple_restaurant(file_list[i], contents)

	print("done!")