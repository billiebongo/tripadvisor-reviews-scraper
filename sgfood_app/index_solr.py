
from .models import Restaurant, Review
import json
from .clean_data import clean_review
import os
json_saved_path='json/'


def dump_dict_to_json_file(rest_name, json_contents):
	json_filename = json_saved_path+rest_name+'.json'
	with open(json_filename, 'w') as fp:
		print(json_contents)
		json.dump(json_contents, fp)
		#dump to where????
	return json_filename

def create_json(restaurant):
	reviews=Review.objects.filter(restaurant=restaurant)

	#js=[]
	r_dict={}
	r_dict["rest_name"]=restaurant.rest_name
	r_dict["id"]=restaurant.id
	r_dict["url"]=restaurant.url
	r_dict["total_score"]=restaurant.total_score
	r_dict["price"]=restaurant.price
	r_dict["food_score"]=restaurant.food_score
	r_dict["service_score"]=restaurant.service_score
	r_dict["value_score"]=restaurant.value_score
	r_dict["ambience_score"]=restaurant.ambience_score
	
	r_dict["path"]="1.restaurants"
	_childDocuments_=[]
	for review in reviews:
		review_dict={}
		review_dict["id"]=review.id
		review_dict["score"]=review.score
		review_dict["reviewer"]=review.reviewer
		review_dict["review_body"]=" ".join(clean_review(review.review_body))
		review_dict["path"]="2.restaurants.reviews"

		_childDocuments_.append(review_dict)
	r_dict["_childDocuments_"]=_childDocuments_
	#js.append(r_dict)
	#print(js)
	return r_dict

def create_burpple_json(restaurant):
	reviews=Review.objects.filter(restaurant=restaurant)

	#js=[]
	r_dict={}
	r_dict["rest_name"]=restaurant.rest_name
	r_dict["id"]=restaurant.id
	r_dict["url"]=restaurant.url
	r_dict["path"]="1.restaurants"
	_childDocuments_=[]
	for review in reviews:
		review_dict={}
		review_dict["id"]=review.id
		review_dict["reviewer"]=review.reviewer
		review_dict["review_body"]=" ".join(clean_review(review.review_body))
		review_dict["path"]="2.restaurants.reviews"

		_childDocuments_.append(review_dict)
	r_dict["_childDocuments_"]=_childDocuments_
	#js.append(r_dict)
	#print(js)
	return r_dict

def post_(r_dict):
	format_dict={}
	format_dict["doc"]=r_dict
	post_dict={}
	post_dict["add"]=format_dict
	q=json.dumps(post_dict)
	command="curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/food/update' -d '"+q+"'"
	print(command)
	os.system(command)

	return

def run_script():
	restaurants=Restaurant.objects.all()
	for restaurant in restaurants:
		js=create_json(restaurant)
	#print(js)
		post_(js)
	return
	#json_filename = dump_dict_to_json_file(rest.rest_name.replace(" ","_"),js)



	#322585