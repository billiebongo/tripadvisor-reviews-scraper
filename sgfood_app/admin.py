from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Restaurant, Review)
from django.contrib.auth.admin import UserAdmin


class RestaurantAdmin(admin.ModelAdmin): 
  list_display = ('total_score','rest_name')
class ReviewAdmin(admin.ModelAdmin): 
  list_display = ('review_body','restaurant','score', 'reviewer')


#admin.site.register(User, UserAdmin)



admin.site.register(Restaurant, RestaurantAdmin)

admin.site.register(Review, ReviewAdmin)