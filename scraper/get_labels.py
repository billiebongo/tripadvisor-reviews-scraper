# add in the reviews

from requests import Session
import requests
from math import ceil
from bs4 import BeautifulSoup

# Retrieve labels for all restaurants
# Labels are (per restaurant) Price, Food, Service, Value, Ambience
# ratings for each restaurant on TripAdvisor

URL_SET_LIST = "url_set_2.txt"

def get_rest_dets_for_rest(BASE_URL): #given base URL, output all the reviews
	""" Parse restaurant page for rating details for each restaurant """
	# this step should have been done during the scraping of reviews for each restaurant
	# but the full documents were not stored and it would be too consuming to rebuild
	# a process that scrapes the more efficient process
	print("visiting {}".format(BASE_URL))

	session = Session()
	#get first page reviews+page no
	session.head(BASE_URL) #'https://www.burpple.com/mizzy-corner-nasi-lemak/reviews'
	response = session.get(url=BASE_URL)
	soup = BeautifulSoup(response.content, "html.parser")
	#get the num of pages (string time) as well. page 8 is 70

	that_section=soup.find("div", {"class": "ppr_priv_restaurants_detail_info_content"})
	price_section=that_section.find("span", ["ui_column","is-6 price"]).text
	ratings_section=that_section.find("div", {"class": "questionRatings"}).findAll("span")
	for rat in ratings_section:
		print(rat['class'])
	print(price_section)
	print(ratings_section)


def visit_each_rest(): #loop each of the 9k+ restaurants
	with open(URL_SET_LIST) as f: #first 1000 links
		content = f.readlines()
		content = [x.strip() for x in content]
		for i in range(len(content)):
			get_rest_dets_for_rest("https://www.tripadvisor.com.sg{}".format(content[i]))

if __name__ == '__main__':
	#for testing
	get_reviews_for_rest("https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d5421276-Reviews-L_Atelier_Tiramisu-Singapore.html")
