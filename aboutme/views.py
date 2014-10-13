from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template import Context, Template
from django.template.defaultfilters import escape
from tenthings.aboutme.models import Person
from tenthings.aboutme.models import Person, Thing, Comment, Friend
import re
import json
import os
import string
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings
from PIL import Image, ImageFile
from django.contrib.auth.models import User
import pdb
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import shutil
# Resources
# Python debugger: http://ericholscher.com/blog/2008/aug/31/using-pdb-python-debugger-django-debugging-series-/
	
def index(request):
	#this is a test, index page will be login
	#pdb.set_trace()
	person_list = Person.objects.all().order_by('name')
	#this_person = Person.objects.filter(id=request.user.id)
	thing_list = Thing.objects.all()
	#count = 10 - thing_list.count()
	#blanks = range(thing_list.count(),10)
	return render_to_response('aboutme/index.html',
							{'person_list':person_list, 'thing_list':thing_list})


# @login_required							
# def search(request):
	#pdb.set_trace()
	# person_list = Person.objects.all()
	# return render_to_response('aboutme/search.html', locals(), context_instance=RequestContext(request))
	
@login_required
def myaccount(request, person, template_name="aboutme/index.html"):	
	""" User profile.  """
	# if person <> me, then I am looking for a friends profile, make sure we are friends and then let me see their page
	#pdb.set_trace()
	if person == request.user.username:
		thing_list =  Thing.objects.filter(person=request.user)
		comment_list = Comment.objects.filter(person=request.user)
		things = Thing.objects.filter(person=request.user)
		person_id = User.objects.filter(username=request.user) # is this used for anything, person_id is not the id, its the name :(
		personid = request.user.id
		has_photo = get_object_or_404(Person, username=request.user.id)
		name = request.user.username
		#pdb.set_trace()
		friend_list =  Friend.objects.filter(person=request.user.id)
		#return render_to_response('/%s/'%person_id, locals(), context_instance=RequestContext(request))
		return render_to_response(template_name, locals(), context_instance=RequestContext(request))
	else:
		#uUser = User.objects.all().filter(username=person)
		uUser = get_object_or_404(User, username=person)
		thing_list =  Thing.objects.filter(person=person)
		comment_list = Comment.objects.filter(person=uUser.id)
		things = Thing.objects.filter(person=person)
		person_id = User.objects.filter(username=person)
		personid = uUser.id
		has_photo = get_object_or_404(Person, username=uUser.id)
		name = person		
		friend_list =  Friend.objects.filter(person=uUser.id)
		#friend_list =  get_object_or_404(Friend, person=uUser.id)
		return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def my_view(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			HttpResponseRedirect('/%s/'%username) 
		else:
			error = 'account disabled'
	else:
		error = 'invalid login'
		
	
def save(request):
    try:
		#pdb.set_trace()
		
		# hmm, can't get base.html to pass personid to request.POST request.POST[u'personid'], so how to I get the login ID?
		# this should be easy, I must be just not seeing it. Try person or id
		# Ok, that WAS easy!  when user is logged in, HttpRequest.user contains user as per: http://docs.djangoproject.com/en/dev/ref/request-response/		
		t = Thing(pk=request.POST[u'id'], thing_count=request.POST[u'id'], thingsAboutMe=request.POST[u'value'], person=request.user.username, person_id=request.user.id)		
		t.save()
		html_id = request.POST[u'id']
		value = request.POST[u'value']	
		return HttpResponse(escape(value))		
    except:
        html_id = request.GET[u'id']
        value = request.GET[u'value']
    if not re.match(ur'^\w+$', html_id):
        raise Exception(u'Invalid HTML id.')
	#strValue = u'('+ str(html_id) + u') changed by: ' + request.user.username + u' to: ' + value + u'\n'
	return HttpResponse(escape(value))
	

def save_comment(request):
    #try:
		#pdb.set_trace()		
	#request.session['thing_id'] = True
	t = get_object_or_404(Thing, pk=request.POST[u'id'])
	# Commenter is the person who is logged in and commenting on their friends post
	# Person is the one getting the comment, friend relationship not in place yet
	# but should be from Friend table, where person_id is me and friend_id is the friend i'm going to comment on
	#f = Friend.objects.filter(friend=t.person_id)  #request.friend
	# TO DO:  person_id=f[0].id
	# Person_id is is the person recieving the comment
	#### s = request.user.username + " said: " + request.POST[u'value']
	s = request.POST[u'value']
	c = Comment(thing_id=t.id, comment=s,friend_id=request.user.id,person_id=t.person_id) #f[0].id is the id in friend table that contains your friend		
	c.save()
	html_id = request.POST[u'id']
	value = request.POST[u'value']
	name = request.user.username
	#return HttpResponse(escape(value))		
	#return HttpResponseRedirect(reverse('tenthings.aboutme.views.myaccount', args=(request.user.username,)))
	#return render_to_response('aboutme/myaccount.html', locals(), context_instance=RequestContext(request))
	#return HttpResponseRedirect(reverse('tenthings.aboutme.views.myaccount', args=(name,)))
    #except:
    #    html_id = request.GET[u'id']
    #    value = request.GET[u'value']
    #if not re.match(ur'^\w+$', html_id):
    #    raise Exception(u'Invalid HTML id.')
	#strValue = u'('+ str(html_id) + u') changed by: ' + request.user.username + u' to: ' + value + u'\n'
	return HttpResponse(escape(value))
	
def delete_comment(request):
	#pdb.set_trace()
	c = get_object_or_404(Comment, pk=request.POST[u'id'])
	c.delete()
	name = request.user.username
	#return render_to_response('aboutme/index.html', locals(), context_instance=RequestContext(request))
	return HttpResponseRedirect(reverse('tenthings.aboutme.views.myaccount', args=(name,)))


def resize(file_to_resize, string_id,):
	# Resize the image
	parser = ImageFile.Parser()
	while True:
		s = file_to_resize.read(1024)
		if not s:
			break
		parser.feed(s)
	image = parser.close()

	#ms = Image.open(file_to_resize)
	ms = image.copy()
	size = 320,240
	ms.thumbnail(size, Image.ANTIALIAS)
	#ms.save(settings.MEDIA_ROOT + u'/images/profile/' + string_id, "JPEG") 
	ms.save('site_media/images/profile/' + string_id, "JPEG") 

def copyimage(string_id):
	#os.copy(settings.MEDIA_ROOT + u'/images/profile/guy.GIF', settings.MEDIA_ROOT + u'/images/profile/' + string_id)
	#pdb.set_trace()
	#spath=settings.MEDIA_ROOT + u'/images/profile/'
	#shutil.copyfile(spath+'guy.GIF', spath + str(string_id))
	p = os.path.abspath('public//site_media//images//profile//') + str(string_id)
	#shutil.copyfile(os.path.abspath('public//site_media//img//guy.GIF'),  settings.MEDIA_ROOT + u'/images/profile/' + str(string_id))
	shutil.copyfile(os.path.abspath('site_media//img//guy.GIF'),  os.path.abspath('site_media//images//profile//' + str(string_id)))
	# try	
		# shutil.copy2(settings.MEDIA_ROOT + u'//images//profile//guy.GIF',  settings.MEDIA_ROOT + u'//images//profile//' + str(string_id))
	# except IOError as e:
		# print e
	
def saveimage(request, string_id):
	#pdb.set_trace()
	id = int(string_id)
	#entity = Person.objects.filter(id = id)[0]
	entity = Person.objects.filter(username = id)[0]
	original_mimetype = entity.image_mimetype
	file = request.FILES.values()[0]
	extension = file.name.lower().split(".")[-1]
	if extension == u'jpg':
		entity.image_mimetype = u'image/jpeg'
	elif extension == u'swf':
		entity.image_mimetype = u'application/x-shockwave-flash'
	else:
		entity.image_mimetype = u'image/' + extension
	entity.save()
	try:        
		os.remove(settings.MEDIA_ROOT + u'/images/profile/' + string_id)
		os.rename(settings.MEDIA_ROOT + u'/images/profile/' +
			string_id, settings.MEDIA_ROOT + u'/images/profile/' +
			string_id + '.old')
	except OSError:		
		pass	
	resize(file, string_id)
	result = u'''<img class="profile" src="/images/%d">''' % id # + \
	has_photo = get_object_or_404(Person, username = request.user.id)
	thing_list =  Thing.objects.filter(person=request.user)
	person_id = User.objects.filter(username=request.user)
	name = request.user.username
	#http://stackoverflow.com/questions/1335898/django-httpresponseredirect-reverse-function-in-tutorial
	#The reverse function has access to the URL map that Django uses to find 
	#a view function for incoming URLs. In this case, you pass in a view function, 
	#and the arguments it will get, and it finds the URL that would map to it. 
	#Then the HttpResponseRedirect function creates a response that directs 
	#the browser to visit that URL.
	#This is a way of saying, "Now call the mysite.polls.views.results view."
	return HttpResponseRedirect(reverse('tenthings.aboutme.views.myaccount', args=(name,)))
	#return render_to_response('aboutme/index.html', locals(), context_instance=RequestContext(request))
	#return render_to_response('aboutme/index.html', {'person_list':person_list, 'thing_list':thing_list})

@login_required							
def addfriend(request, fid):
	#pdb.set_trace()
	f = Friend(friend_id=fid, person_id=request.user.id) #f[0].id is the id in friend table that contains your friend		
	f.save()
	return render_to_response('aboutme/index.html', locals(), context_instance=RequestContext(request))

	
def searchpage(request):
	return render_to_response('aboutme/search.html', locals(), context_instance=RequestContext(request))
	
def search(request):
	#pdb.set_trace()
	query_string = ''
	found_friends = None
	#if (request.POST.count = 0):
#		query_string = 'a'
#		friend_query = get_query(query_string, ['username','email',])
	#else 
	#if ('q' in request.POST) and request.POST['q'].strip():
	if (request.method == 'POST'):
		if ('q' in request.POST) and request.POST['q'].strip():
			query_string = request.POST['q']    
			if (query_string == ''):
				query_string = 'a'
			friend_query = get_query(query_string, ['username','email',])
			found_friends = User.objects.filter(friend_query).order_by('username')
	
	if (found_friends):
		paginator = Paginator(found_friends, 5,0)		
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
	
		try:
			friend_pages = paginator.page(page)
		except (EmptyPage, InvalidPage):
			friend_pages = paginator.page(paginator.num_pages)		
	else:
		found_friends=u''
	return render_to_response('aboutme/search.html', locals(), context_instance=RequestContext(request))

						  
import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
