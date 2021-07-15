from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import DeleteView
from post.models import Stream, Post, Likes, PostFileContent, Category
from post.forms import NewPostForm, EditPost

from django.contrib.auth.models import User
from comment.models import Comment
from comment.forms import CommentForm

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.urls import reverse, reverse_lazy
from authy.models import Profile

from django.views.decorators.cache import cache_page

# Create your views here.


def index(request):
	user = request.user
	template = loader.get_template('index.html')

	context = {}

	return HttpResponse(template.render(context, request))
@login_required
def PostDetails(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	user = request.user
	profile = Profile.objects.get(user=user)
	favorited = False

	#comment
	comments = Comment.objects.filter(post=post).order_by('date')
	
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=user)
		#For the color of the favorite button

		if profile.favorites.filter(id=post_id).exists():
			favorited = True

	#Comments Form
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = user
			comment.save()
			return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	else:
		form = CommentForm()


	template = loader.get_template('post_detail.html')

	context = {
		'post':post,
		'favorited':favorited,
		'profile':profile,
		'form':form,
		'comments':comments,
	}

	return HttpResponse(template.render(context, request))


@login_required
def NewPost(request):
	user = request.user
	cat_objs = []
	files_objs = []
	

	if request.method == 'POST':
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			files = request.FILES.getlist('content')
			title = form.cleaned_data.get('title')
			caption = form.cleaned_data.get('caption')
			category = form.cleaned_data.get('category')
			#creative_skills = form.cleaned_data.get('creative_skills')
			state = form.cleaned_data.get('state')
			city = form.cleaned_data.get('city')
			cost = form.cleaned_data.get('cost')
			address = form.cleaned_data.get('address')
			parcel = form.cleaned_data.get('parcel')
			#add_category = form.cleaned_data.get('add_category')
			#cat_list = list(add_category.split(','))
			
			if parcel==True:
				parcel = True
			else:
				parcel = False
			
			#for cat in cat_list:
			#	c,created = Category.objects.update_or_create(name=cat)
			
			#	cat_objs.append(c)
			

			for file in files:
				file_instance = PostFileContent(file=file, user=user)
				file_instance.save()
				files_objs.append(file_instance)

			p, created = Post.objects.get_or_create(caption=caption,title=title, user=user,state=state,city=city,address=address,cost=cost,category=category,parcel=parcel,status=False,feedback='None',suggestions='None')
			#p.category.set(cat_objs)
			p.content.set(files_objs)
			p.save()
			return redirect('home')
	else:
		form = NewPostForm()

	context = {
		'form':form,
	}

	return render(request, 'newpost.html', context)

def category(request, category_slug):
	category = get_object_or_404(Category, slug=category_slug)
	posts = Post.objects.filter(category=category, status=False).order_by('-posted')

	template = loader.get_template('categories.html')

	context = {
		'posts':posts,
		'category':category,
	}

	return HttpResponse(template.render(context, request))



@login_required
def like(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(user=user, post=post).count()

	if not liked:
		like = Likes.objects.create(user=user, post=post)
		like_status = True
		#like.save()
		current_likes = current_likes + 1

	else:
		Likes.objects.filter(user=user, post=post).delete()
		like_status = False
		current_likes = current_likes - 1

	post.likes = current_likes
	post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))

@login_required
def favorite(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)

	else:
		profile.favorites.add(post)

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))


class DeletePostView(DeleteView):
	model = Post
	template_name  = 'delete_post.html'
	succes_url = reverse_lazy('index')

@login_required
def explorebooks(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		posts = Post.objects.filter(Q(caption__icontains=query)|
									Q(title__icontains=query)|
									Q(category__icontains=query),status=False)
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
	
	template = loader.get_template('explore_books.html')
	
	return HttpResponse(template.render(context, request))


def CategoryView(request, cats):
	category_posts = Post.objects.filter(category=cats.replace('-',' '),status=False)
	return render(request, 'categories.html', {'category_posts':category_posts})

	
def update_status(request,post_id):
	post = get_object_or_404(Post, id=post_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	if request.method == 'POST':
		form = EditPost(request.POST)
		if form.is_valid():
			status = form.cleaned_data.get('status')
			feedback = form.cleaned_data.get('feedback')
			suggestions = form.cleaned_data.get('suggestions')

			post.status = status
			post.feedback = feedback
			post.suggestions = suggestions
			post.save()
			return redirect('home')
	else:
		form = EditPost(instance=post)
		

	context = {
		'form':form,
	}

	return render(request, 'editstatus.html', context)



		




