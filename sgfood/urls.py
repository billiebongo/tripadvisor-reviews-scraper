from django.conf.urls import url
from django.contrib import admin
from sgfood_app.views import *

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
	url(r'^admin/', admin.site.urls),
    url(r'^home/$', home, name='home'),
    url(r'^results/$', results, name='res'),

]
