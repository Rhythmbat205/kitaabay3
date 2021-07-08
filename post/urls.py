from django.urls import path
from post.views import index, NewPost, PostDetails, like, favorite, DeletePostView,CategoryView,explorebooks,update_status
from explore.views import home

urlpatterns = [
	#path('exploreposts',exploreposts, name='exploreposts'),
   	#path('', index, name='index'),
	path('<uuid:post_id>/edit', update_status, name='editpost'),
	path('category/<str:cats>/', CategoryView, name='category'),
	path('', home, name='home'),
   	path('newpost/', NewPost, name='newpost'),
   	path('<uuid:post_id>', PostDetails, name='postdetails'),
   	path('<uuid:post_id>/like', like, name='postlike'),
   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
	path('<uuid:post_id>/', DeletePostView.as_view(), name='delete_post'),
	
	path('explorebooks',explorebooks, name='explorebooks'),

]