from django import forms
from post.models import Post,Category

from django.forms import ClearableFileInput

'''
choices = [('All', 'All'),
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
	('Physical Education', 'Physical Education')]
'''
choices=Category.objects.all().values_list('name','name')

choice_list=[]
for items in choices:
	choice_list.append(items)


class NewPostForm(forms.ModelForm):
	content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
	title = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-small','placeholder':'Title'}), required=True)
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-large','placeholder':'Description'}), required=True)
	#category = forms.CharField(widget=forms.Select(choices=choice_list ,attrs={'class': 'input is-medium'}), required=True)
	#add_category = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=False)
	state = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-small','placeholder':'State'}), required=True)
	city = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-small','placeholder':'City'}), required=True)
	address = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium','placeholder':'Your Complete Address'}), required=True)
	cost = forms.IntegerField()
	category = forms.CharField(widget=forms.Select(choices=choice_list, attrs={'class': 'input is-small'}), required=True)
	parcel = forms.BooleanField(required=False)

	class Meta:
		model = Post
		fields = ('content', 'title', 'caption','category','state','city','address','cost','parcel')
		

class EditPost(forms.ModelForm):
	status = forms.BooleanField(required=False)
	feedback = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium','placeholder':'Your Feedback'}), required=True)
	suggestions = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium','placeholder':'Your Suggestions'}), required=True)

	class Meta:
		model = Post
		fields = ('status','feedback','suggestions')
		