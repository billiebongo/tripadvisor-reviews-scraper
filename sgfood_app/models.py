from django.db import models


class Review(models.Model):
	restaurant = models.ForeignKey('Restaurant', related_name='reviews', on_delete=models.CASCADE, null=True)
	review_body = models.CharField(max_length=500, blank=False)
	score = models.FloatField(null=True)
	reviewer = models.CharField(max_length=30, blank=False, null=True)

class Restaurant(models.Model):
	rest_name = models.CharField(max_length=50, blank=False)
	url = models.CharField(max_length=100, null=True)
	total_score = models.FloatField(null=True)
	food_score = models.FloatField(null=True)
	service_score = models.FloatField(null=True)
	price=models.IntegerField(null=True) 
	value_score = models.FloatField(null=True)
	ambience_score = models.FloatField(null=True)
	#lat = models.FloatField(null=True)
	#lon = models.FloatField(null=True)
	#address = models.CharField(max_length=50, null=True) #MRT
