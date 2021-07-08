from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authy.models import Profile
from PIL import Image
def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')

class SignupForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
	email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True,)
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

	class Meta:

		model = User
		fields = ('username', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		self.fields['email'].validators.append(UniqueEmail)

	def clean(self):
		super(SignupForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
		return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data
from django.core.files.storage import default_storage as storage
class EditProfileForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	url = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
	profile_info = forms.CharField(widget=forms.TextInput(), max_length=260, required=False)
	
	
	
	class Meta:
		model = Profile
		fields = ('first_name', 'last_name', 'profile_info')



		

	'''		
	def save(self):
		profile = super(EditProfileForm,self).save()
		
		profile.first_name = self.cleaned_data.get('first_name')
		profile.last_name = self.cleaned_data.get('last_name')
		profile.location = self.cleaned_data.get('location')
		profile.url = self.cleaned_data.get('url')
		profile.profile_info = self.cleaned_data.get('profile_info')
		profile.occupation = self.cleaned_data.get('occupation')
		profile.twitter_url = self.cleaned_data.get('twitter_url')
		profile.instagram_url = self.cleaned_data.get('instagram_url')
		profile.youtube_url = self.cleaned_data.get('youtube_url')
		profile.linkedin_url = self.cleaned_data.get('linkedin_url')
		profile.facebook_url = self.cleaned_data.get('facebook_url')
		

		image = Image.open(profile.picture)
		resized_image = image.resize((250, 250), Image.ANTIALIAS)
		fh = storage.open(profile.picture.name, "w")
		picture_format = 'png'
		resized_image.save(fh, picture_format)
		fh.close()        
		resized_image.save(profile.picture.path)
		return profile
	'''

		




