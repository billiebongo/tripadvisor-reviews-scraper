from requests import Session

from bs4 import BeautifulSoup
session = Session()

##############################
#
# Collects directory to 7000+ Restaurants in Singapore and no of reviews per rest
# Outputs url_list.txt
#
##############################



def scrape_reviews(page_no):
	""" """
	# this is the SEED_URL with pages directing to individual restaurants
	REST_URL = 'https://www.tripadvisor.com.sg/Restaurants-g294265-Singapore.html'
	session.head(REST_URL) #'https://www.burpple.com/mizzy-corner-nasi-lemak/reviews'

	response = session.get(
		#reminder: url is not for browser navigation, its request API call
		url='https://www.tripadvisor.com.sg/RestaurantSearch?Action=PAGE&geo=294265&ajax=1&sortOrder=relevance&o=a{}&availSearchEnabled=false'.format(page_no), #count min 0 and increment by 20
		headers={
			'Referer': "https://www.tripadvisor.com.sg/Restaurants-g294265-Singapore.html"
		}
	)
	soup = BeautifulSoup(response.content, "html.parser")

	for i in range(30):
		if (i==0):
			index_count_class="listing rebrand listingIndex-"+str(int(i+1))+" first"
		else:

			index_count_class="listing rebrand listingIndex-"+str(int(i+1))

		key=soup.find("div", {"class": index_count_class})
		anchor_tag=key.find("a")['href']
		print(anchor_tag)
		#review_count= key.find("span", {"class": "reviewCount"}).text.strip()[:-8]
		#print(review_count)
		#review count in tripadvisor on front page is not updated zz
	return

def go_each_page():
	for p in range(262): #only until page 263 got reviews, restaurants somewhat ordered by number of reviews?
		page_no = p*30 # 30 restaurants in each page.
		scrape_reviews(str(page_no))
	return

if __name__ == '__main__':
	go_each_page()
