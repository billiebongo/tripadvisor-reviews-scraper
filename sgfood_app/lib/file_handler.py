import os

"""
Helper functions to retrieve reviews from burrple textfiles
"""

DATA_DIR='sgfood_app/data/burpple/burp' #change to TA for TA loading

def find_files_in_dir():

	#print(os.listdir('data/TA/'))
	#files=os.listdir()

	file_list = [f[:-4] for f in os.listdir(DATA_DIR) if  f[-4:]=='.txt'] #os.path.isfile(f) and
	return file_list #no .txt

def check_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_ratings_reviews_from_textfile(filename): 
	""" Open textfule return list of ratings and reviews (ordered) """
	contents=[]

	filename="{}/{}.txt".format(DATA_DIR,filename)
	with open(filename) as f:
		content = f.readlines() 
		contents += [x.strip() for x in content]
	
	ratings=[]
	reviews=[]
	i=0 #line pointer

	while i<(len(contents)):
		if len(contents[i])==1 and check_int(contents[i])==True:#assuming review is len==1
			ratings.append(contents[i])
			i+=1
			reviews.append(contents[i])
			i+=1
		else:
			last_review_position=len(reviews)-1
			reviews[last_review_position]=reviews[last_review_position]+contents[i]
			i+=1
	return ratings, reviews

def get_burple_reviews(filename):
	""" given filename return file contents """
	contents=[]

	filename="{}/{}.txt".format(DATA_DIR,filename)
	print(filename)
	with open(filename) as f:
		content = f.readlines() 
		if len(content) > 1:
			print("not empty")
			contents += [x.strip() for x in content]
		else: # Some files seem to be empty? no reviews?
			print("empty file")

	return contents