"""instagram_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from explore.views import home
from django.conf.urls import url
from django.views.static import serve
from authy.views import UserProfile, UserProfileFavorites, follow,sold_books
from post.views import index
urlpatterns = [
    path('',index,name='index'),
    path('notifications/', include('notifications.urls')),
    path('explore/', include('explore.urls')),
    path('home/',home, name='home'),
    path('direct/', include('direct.urls')),
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('user/', include('authy.urls')),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/saved', UserProfile, name='profilefavorites'),
    path('<username>/follow/<option>', follow, name='follow'),
    path('<username>/sold',sold_books,name='soldbooks' )
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
