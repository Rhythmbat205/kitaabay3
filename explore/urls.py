from django.urls import path
from explore.views import home, exploreuser,exploreposts,aboutus

urlpatterns = [
   	#path('', home, name='home'),
	path('exploreuser',exploreuser, name='exploreuser'),
	path('exploreposts',exploreposts, name='exploreposts'),
	path('aboutus',aboutus,name='aboutus'),
	#path('allposts/',allposts, name='allposts'),
]