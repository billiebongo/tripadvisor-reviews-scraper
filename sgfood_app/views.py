from django.shortcuts import render, render_to_response

from django.http import JsonResponse
from datetime import date
import requests
#
from .query import query_solr
from .models import Restaurant, Review
# Create your views here.

def get_review(rests):
	for rest in rests:
		if "childDocuments" in rest:
			for rev in rest["childDocuments"]:
				#print(rev["id"])
				#print(Review.objects.get(id=rev["id"]).review_body)
				rev["review_body"]=Review.objects.get(id=rev["id"]).review_body
	return rests


def results(request):
	''' This could be your actual view or a new one '''
	# Your code
	if (request.method == 'GET') and ('search_box' in request.GET): # If the form is submitted

		query = request.GET.get('search_box', None)
		print(query)
		results=query_solr(query)
		rests=get_review(results["response"]["docs"])
		
		return render(request, 'results.html', {'query': query, 'results':rests})
	return JsonResponse({'hello': 'search box was empty'})

def home(request):
	''' This could be your actual view or a new one '''
	# Your code
	return render(request, 'homepage.html')

