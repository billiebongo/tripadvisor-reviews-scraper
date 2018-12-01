#import pandas as pd
#from .models import Review




#def run_script():
#	reviews = Review.objects.all()
#	df = pd.DataFrame()
#	c=0
#	for review in reviews:
#		print(c)
#		df=df.append({'id':review.id,'review_body':review.review_body, 'rating': review.score}, ignore_index=True)
#		c+=1
#	df.to_csv('all_reviews.csv', sep='\t')