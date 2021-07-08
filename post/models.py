import uuid
from django.db import models
from django.contrib.auth.models import User

from multiselectfield import MultiSelectField
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse

from notifications.models import Notification

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


		
		
	

'''	
categories = (
	('All', 'All'),
	('Novel','Novel'),
	('10+1', '10+1'),
	('10+2', '10+2'),
	('10th', '10th'),
	('B.Arch', 'B.Arch'),
	('B.Com', 'B.Com'),
	('B.Des', 'B.Des'),
	('B.Ed', 'B.Ed'),
	('B.Lib.Sc', 'B.Lib.Sc'),
	('B.Pharmacy', 'B.Pharmacy'),
	('B.Sc', 'B.Sc'),
	('B.Sc Agriculture', 'B.Sc Agriculture'),
	('B.Tech', 'B.Tech'),
	('B.V.Sc', 'B.V.Sc'),
	('BA', 'BA'),
	('BAMS', 'BAMS'),
	('BBA', 'BBA'),
	('BCA', 'BCA'),
	('BDS', 'BDS'),
	('BFA', 'BFA'),
	('BHMS', 'BHMS'),
	('BMC', 'BMC'),
	('BPEd', 'BPEd'),
	('BPT', 'BPT'),
	('BSW', 'BSW'),
	('DM', 'DM'),
	('LLB', 'LLB'),
	('LLM', 'LLM'),
	('M.Arch', 'M.Arch'),
	('M.Ch', 'M.Ch'),
	('M.Com', 'M.Com'),
	('M.Design', 'M.Design'),
	('M.Ed', 'M.Ed'),
	('M.Lib.Sc', 'M.Lib.Sc'),
	('M.Pharm', 'M.Pharm'),
	('M.Phil', 'M.Phil'),
	('M.Sc', 'M.Sc'),
	('M.Sc Agriculture', 'M.Sc Agriculture'),
	('M.Tech', 'M.Tech'),
	('M.V.Sc', 'M.V.Sc'),
	('MA', 'MA'),
	('MBA', 'MBA'),
	('MBBS', 'MBBS'),
	('MCA', 'MCA'),
	('MD', 'MD'),
	('MDS', 'MDS'),
	('MFA', 'MFA'),
	('MMC / MMM', 'MMC / MMM'),
	('MPT', 'MPT'),
	('MS', 'MS'),
	('MSW / MA (SW)', 'MSW / MA (SW)'),
	('Nursing', 'Nursing'),
	('Pharm.D', 'Pharm.D'),
	('PhD', 'PhD'),
	('Physical Education', 'Physical Education'),
)
'''
class PostFileContent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
	file = models.FileField(upload_to=user_directory_path)
	
class Category(models.Model):
	name=models.CharField(max_length=100)

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('home')

class Post(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	content =  models.ManyToManyField(PostFileContent, related_name='contents')
	title = models.TextField(max_length=50, verbose_name='title',default='title')
	caption = models.TextField(max_length=1500, verbose_name='Caption')
	#category = MultiSelectField(choices=categories,default='All')
	#category = models.ManyToManyField(Category, related_name='categories')
	category = models.CharField(max_length=100,default='novel')
	cost = models.IntegerField(default=0)
	posted = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	state = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)
	parcel = models.BooleanField()
	status = models.BooleanField()
	feedback = models.CharField(max_length=150, blank=True,default='None')
	suggestions = models.CharField(max_length=150,  blank=True,default='None')

	def get_absolute_url(self):
		return reverse('postdetails', args=[str(self.id)])


		
		
	def __str__(self):
		return str(self.id)

	

class Follow(models.Model):
	follower = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='follower')
	following = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='following')

	def user_follow(sender, instance, *args, **kwargs):
		follow = instance
		sender = follow.follower
		following = follow.following
		notify = Notification(sender=sender, user=following, notification_type=3)
		notify.save()

	def user_unfollow(sender, instance, *args, **kwargs):
		follow = instance
		sender = follow.follower
		following = follow.following

		notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
		notify.delete()

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
    	post = instance
    	user = post.user
    	followers = Follow.objects.all().filter(following=user)
    	for follower in followers:
    		stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
    		stream.save()

class Likes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()


#Stream
post_save.connect(Stream.add_post, sender=Post)

#Likes
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unlike_post, sender=Likes)

#Follow
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)