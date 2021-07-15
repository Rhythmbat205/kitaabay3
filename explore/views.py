from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from post.models import Stream, Post,Category
from post.forms import NewPostForm

from django.contrib.auth.models import User
from comment.models import Comment
from comment.forms import CommentForm
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from authy.models import Profile
from django.views.decorators.cache import cache_page


def home(request):
    user = request.user
    posts = Post.objects.filter(status=False)
    
	
    group_ids = []
    for post in posts:
        group_ids.append(post.id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    template = loader.get_template('home.html')
    cat_menu = Category.objects.all()
    context = {
		'post_items': post_items,
		'cat_menu':cat_menu,

	}
    return HttpResponse(template.render(context, request))


    #post_items = Post.objects.all().order_by('-posted')

@login_required
def exploreuser(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))
		profile = Profile.objects.filter(user=users)
		
		#Pagination
		paginator = Paginator(users, 25)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
				'profile':profile,
			}
	
	template = loader.get_template('explore/explore_user.html')
	
	return HttpResponse(template.render(context, request))

@login_required
def exploreposts(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		posts = Post.objects.filter(Q(caption__icontains=query), status=False)
		users= User.objects.filter(post=posts)
		profile = Profile.objects.filter(user=users)
		#Pagination
		paginator = Paginator(posts, 25)
		page_number = request.GET.get('page')
		posts_paginator = paginator.get_page(page_number)

		context = {
				'posts': posts_paginator,
				'profile':profile,
				
			}
	
	template = loader.get_template('explore/explore_posts.html')
	
	return HttpResponse(template.render(context, request))

def aboutus(request):
	context = {}
	template = loader.get_template('aboutus.html')
	
	return HttpResponse(template.render(context, request))

