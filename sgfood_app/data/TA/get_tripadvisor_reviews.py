
 
from requests import Session
import requests
from math import ceil
from bs4 import BeautifulSoup

############################################
#
# Collects all the reviews for each restaurant in url_list.txt
# Outputs rest-name.txt(lower case and "-" for whitespace) for each restaurant
#
############################################


def expand_mores(REVIEW_ID_LIST): #review_id is unique, regardless of restaurant
	expanded_reviews_list=[]
	for i in range(len(REVIEW_ID_LIST)):
		REVIEW_ID_LIST[i]=REVIEW_ID_LIST[i][7:]

	review_id_string = ",".join(REVIEW_ID_LIST)
	session = Session()
	url='https://www.tripadvisor.com.sg/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS&metaReferer=Restaurant_Review'

	REST_URL = url
	session.head(REST_URL)
	form_data={
		'Action':'install',
		'haveCsses':'long_lived_global_legacy,location_detail_rebrand',
		'haveJses':'global_error,amdearly,jquery,mootools,tripadvisor,eatery-detail-2col,desktop-calendar-templates-dust-en_SG,long_lived_global_legacy,short_lived_global_legacy,taevents',
		'reviews': review_id_string,
		'widgetChoice':'EXPANDED_HOTEL_REVIEW_HSX',
	}

	response=requests.post(url, data=form_data)

	soup = BeautifulSoup(response.content, "html.parser")
	#full_reviews = soup.findAll("div", {"class": "prw_rup prw_reviews_text_summary_hsx"})
	full_reviews = soup.findAll("div", {"class": "prw_rup prw_reviews_basic_review_hsx"})

	for full_review in full_reviews:
		rating=full_review.find("div",["reviewItemInline"]).find("span")['class'][1]
		print(rating[-2:0])
		if (rating[-2:]==str(40)):
			rating=4
		elif rating[-2:]==str(50):
			rating=5
		elif rating[-2:]==str(30):
			rating=3
		elif rating[-2:]==str(20):
			rating=2
		elif rating[-2:]==str(10):
			rating=1
		else:
			rating=0
		expanded_reviews_list.append(str(rating))
		full_review=full_review.find("div",["entry"])
		expanded_reviews_list.append(full_review.text[:-10])
	return expanded_reviews_list



def check_url(): #checks "Reviews-" only appears once in URL, which might crash scraping script later on in 2 parts
	with open("test_url_list.txt") as f:
		content = f.readlines()
		content = [x.strip() for x in content]
		for i in range(len(content)):
			one_only=content[i].count('Reviews-')
			if one_only>1:
				print("ERROR: Reviews- occurred more than once in the URL-{}".format())
				return False
			else:
				print("ok")
		return True

def produce_text_file_per_rest(rest_name, reviews_list):
	filename=rest_name+".txt"
	with open(filename, 'w') as f:
		for review in reviews_list:
			f.write(review + '\n')
	return

def scrape_reviews(soup):
	ALL_REVIEWS_DUMP_PER_PAGE = [] #per unique rest
	mores_review_list = [] #reviews with "More.."
	reviews = soup.findAll("div", {"class": "prw_rup prw_reviews_basic_review_hsx"})
	#scrape those without "more"
	for review in reviews:

		if review.find("span", ["ulBlueLinks"]) is not None:
			mores_review_list.append(review.find("div",["reviewSelector"])['id'])
		else:
			rating=review.find("div",["reviewItemInline"]).find("span")['class'][1]
			print(rating)
			if (rating[-2:]==str(40)):
				rating=4
			elif rating[-2:]==str(50):
				rating=5
			elif rating[-2:]==str(30):
				rating=3
			elif rating[-2:]==str(20):
				rating=2
			elif rating[-2:]==str(10):
				rating=1
			else:
				rating=0
			ALL_REVIEWS_DUMP_PER_PAGE.append(str(rating))
			review = review.find("div",["entry"])
			print(review)
			ALL_REVIEWS_DUMP_PER_PAGE.append(review.text)

	expanded_reviews_list = expand_mores(mores_review_list)
	ALL_REVIEWS_DUMP_PER_PAGE = ALL_REVIEWS_DUMP_PER_PAGE + expanded_reviews_list
	return ALL_REVIEWS_DUMP_PER_PAGE



def get_reviews_for_rest(BASE_URL): #given base URL, output all the reviews
	print("going{}".format(BASE_URL))
	ALL_REVIEWS=[]
	session = Session()
	#get first page reviews+page no
	session.head(BASE_URL) #'https://www.burpple.com/mizzy-corner-nasi-lemak/reviews'
	response = session.get(url=BASE_URL)
	soup = BeautifulSoup(response.content, "html.parser")
	#get the num of pages (string time) as well. page 8 is 70
	try:
		last_page=soup.find("div", {"class": "prw_rup prw_common_north_star_pagination "}).find("span", ["last"]).text
	except AttributeError as err:
		print("no last page")
		return
	print(last_page)
	ALL_REVIEWS_DUMP_PER_PAGE=scrape_reviews(soup) #per page of rest
	ALL_REVIEWS=ALL_REVIEWS+ALL_REVIEWS_DUMP_PER_PAGE
	#ONLY RUN THIS IF THERE'S A SECOND PAGE!
	#get subsequent pages
	if last_page is not None:
		#for i in range(1,int(last_page)-1): #72 revieews -> or10(pg2) to or70(pg8)
		for i in range(1,int(last_page)-1):
			session = Session()
			print("at page{}".format(str(i+1)))
			url_head=BASE_URL.split("Reviews-")[0]
			url_tail=BASE_URL.split("Reviews-")[1]
			review_page=url_head+"Reviews-or"+str(i*10)+"-"+url_tail
			#review_page=url_head+"Reviews-or"+str(250)+"-"+url_tail
			session.head(review_page) #'https://www.burpple.com/mizzy-corner-nasi-lemak/reviews'
			response = session.get(url=review_page)
			soup = BeautifulSoup(response.content, "html.parser")
			ALL_REVIEWS_DUMP_PER_PAGE=scrape_reviews(soup) #per page of rest
			ALL_REVIEWS=ALL_REVIEWS+ALL_REVIEWS_DUMP_PER_PAGE
	else:
		print("only one page") #are there reviews in there in the first place?
	
	filename=BASE_URL.split("Reviews-")[1][:-15]
	print("printing all reviews of rest into {}".format(filename))
	produce_text_file_per_rest(filename, ALL_REVIEWS)



def visit_each_rest(): #loop each of the 9k+ restaurants
	with open("url_set_3.txt") as f: #first 1000 links
		content = f.readlines()
		content = [x.strip() for x in content]
		for i in range(len(content)):
			get_reviews_for_rest("https://www.tripadvisor.com.sg{}".format(content[i]))

visit_each_rest()
#get_reviews_for_rest("https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d8027035-Reviews-Llaollao_Natural_Frozen_Yoghurt-Singapore.html")
#expand_mores(["556842400","555751780"])

