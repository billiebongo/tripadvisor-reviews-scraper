#parse results

from find_review_for_restaurant import *



"""
Generating URL for all Burrple restaurants in SG 
"""

def turn_str_to_url(link_string):
	""" Format URL from retrieved restaurant name """
	pre_links = link_string[2:-2].split("', '")
	cleaned_links=[]
	for i in range(10):
		cleaned_links.append(str(pre_links[i].split("?")[0])+"/reviews")
	return cleaned_links

def turn_str_to_venue(venue_string):
	""" Format venue from retrieved string """
	pre_venue = venue_string[2:-2].split("', '")
	cleaned_venue=[]
	for i in range(10):
		cleaned_venue.append(pre_venue[i])
	return cleaned_venue

def save_reviews(rest_name,review_list): #filename=rest_name
	""" Save reviews in textfile named after rest_name """
	filename=rest_name+".txt"
	with open(filename, 'w') as f:
		for review in review_list:
			f.write(review + '\n')
if __name__ == '__main__':

	with open("results2.txt") as f:
		content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]

	#print(turn_str_to_url(content[url_line]))
	#print(turn_str_to_venue(content[2]))
	url_line=0
	venue_line=2

	for loc in range(150): #assuming 150 locations
		real_url_list=turn_str_to_url(content[url_line])
		real_venue_list=turn_str_to_venue(content[venue_line])
		for rest_count in range(10): #for each restaurant in top 10 of location
			list_to_store=scrape_reviews(real_url_list[rest_count],real_venue_list[rest_count])
			print("reviews for "+real_url_list[rest_count]+" at "+ real_venue_list[rest_count]+"scraped")
			save_reviews(real_url_list[rest_count][1:-8], list_to_store)
		url_line+=4
		venue_line+=4
