from tenthings.aboutme.models import Person, Thing
from tenthings.accounts.models import UserCreationFormExtended
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib import messages
from tenthings.aboutme.views import copyimage
import pdb


@login_required
#def my_account(request, template_name="registration/my_account.html"):
def my_account(request,template_name="registration/my_account.html"):
#def my_account(request):
	#pdb.set_trace()
	page_title = 'My Account'
	things = Thing.objects.filter(person=request.user)
	name = request.user.username
	#template_name="aboutme/index.html"
	#return render_to_response(template_name, locals(), context_instance=RequestContext(request))
	# return HttpResponseRedirect(reverse('/',args=[request.user.username]))
	if request.user.is_authenticated() and not request.session.get('homepage_redir'): 
		request.session['homepage_redir'] = True
	return HttpResponseRedirect(reverse('tenthings.aboutme.views.myaccount',args=[request.user.username])) 
	
	

# @login_required
# def myaccount(request, person, template_name="aboutme/index.html"):	
	# """ page displaying customer account information, past order list and account options """
	##pdb.set_trace()
	# page_title = 'My Account'
	# thing_list =  Thing.objects.filter(person=person)
	# things = Thing.objects.filter(person=request.user)
	# name = request.user.username
	# return render_to_response(template_name, locals(), context_instance=RequestContext(request))
	##return render_to_response('aboutme/index.html', {'person_list':person_list, 'thing_list':thing_list})

	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('tenthings.aboutme.views.index'))
	
	
def register(request, template_name="registration/register.html"):	
	#pdb.set_trace()
	if request.method == 'POST':		
		postdata = request.POST.copy()
		form = UserCreationFormExtended(postdata)		
		if form.is_valid():
			form.save()
			user = form.save(commit=False)  # new
			user.email = postdata.get('email','')  # new
			user.save()  # new			
			un = postdata.get('username','')
			pw = postdata.get('password1','')
			from django.contrib.auth import login, authenticate			
			new_user = authenticate(username=un, password=pw)
			#user = authenticate(username=un, password=pw)
			if new_user and new_user.is_active:
			#if user and user.is_active:
				login(request, new_user)
				#login(request, user)
				url = urlresolvers.reverse('my_account')	
				#pdb.set_trace()
				t = Thing()
				t.createInitialThings(new_user.id, un)		
				p = Person()
				p.username_id = user.id
				p.save()
				myPic = copyimage(new_user.id)
				return HttpResponseRedirect(url)			
		else:
			messages.error(request, 'Username is already taken, try again!')
			form = UserCreationFormExtended()	
			form.fields['username'].widget.attrs = {'class':'login_box'}
			form.fields['password1'].widget.attrs = {'class':'login_box'}
			form.fields['password2'].widget.attrs = {'class':'login_box'}
			form.fields['email'].widget.attrs = {'class':'login_box'}
	else:
		#pdb.set_trace()		
		form = UserCreationFormExtended()	
		form.fields['username'].widget.attrs = {'class':'login_box'}
		form.fields['password1'].widget.attrs = {'class':'login_box'}
		form.fields['password2'].widget.attrs = {'class':'login_box'}
		form.fields['email'].widget.attrs = {'class':'login_box'}
	page_title = 'User Registration'
	return render_to_response(template_name, locals(), context_instance=RequestContext(request))
			
def login(request, template_name="registration/login.html"):
	#pdb.set_trace()
	#http://www.nerdydork.com/django-login-form-on-every-page.html
	form = UserCreationFormExtended()	
	form.fields['username'].widget.attrs = {'class':'login_box'}
	form.fields['password1'].widget.attrs = {'class':'login_box'}
	user= request.user
	if request.method == 'POST':
		postdata = request.POST.copy()		
		un = postdata.get('username','')
		pw = postdata.get('password1','')
		from django.contrib.auth import login, authenticate
		user = authenticate(username=un, password=pw)
		if user != None:
			if user.is_active:
				login(request, user)
				url = urlresolvers.reverse('my_account')
				# success
				return HttpResponseRedirect(url)
			else:
				return direct_to_template(request, 'accounts/register.html')		
		else:
			# http://docs.djangoproject.com/en/1.2/ref/contrib/messages/
			messages.error(request, 'Invalid username or password')
	return render_to_response(template_name, locals(), context_instance=RequestContext(request))

# http://www.nerdydork.com/django-login-form-on-every-page.html
def logout_user(request, template_name="registration/login.html"):
	logout(request)
	url = (template_name)
	try:
		del request.session['member_id']
	except KeyError:
		pass
	#return HttpResponse("You're logged out.")
	return HttpResponseRedirect(url)
	#return render_to_response(template_name, locals(), context_instance=RequestContext(request))

