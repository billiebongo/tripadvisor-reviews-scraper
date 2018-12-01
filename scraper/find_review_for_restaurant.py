from requests import Session
from math import ceil

#for each restaurant in burrple scrape the reviews 


session = Session()

# HEAD requests ask for *just* the headers, which is all you need to grab the
# session cookie



def scrape_reviews(DIR_URL, VENUE_ID):
	""" scrape reviews from burpple"""
	clean_reviews = []
	REST_URL = "https://www.burpple.com"+DIR_URL
	session.head(REST_URL) #'https://www.burpple.com/mizzy-corner-nasi-lemak/reviews'

	no_of_ajax_req = ceil(5000/20) #assuming no more than 5000 reviews per restaurants

	for i in range(no_of_ajax_req):
		count = (i+1)*20
		response = session.get(
			url=str('https://www.burpple.com/foods?is_review=true&offset='+str(count)+'&venue_id='+str(VENUE_ID)), #count min 0 and increment by 20
			headers={
				'Referer': REST_URL
			}
		)
		print("calling "+DIR_URL+" at "+VENUE_ID)
		if len(response.text)<3000:
			print(i)
			print("restaurant done")
			break

		splice_term = "food-description-body"
		list_of_reviews = response.text.split(splice_term)[1:]

		for i in range(len(list_of_reviews)):
			review=list_of_reviews[i].split("<\\/p>", 1)[0][6:]
			clean_reviews.append(review)
	
	return clean_reviews

if __name__ == '__main__':
	x=scrape_reviews("https://www.burpple.com/shukuu-izakaya/reviews", 174052)
