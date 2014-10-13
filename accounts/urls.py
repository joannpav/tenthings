from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tenthings.accounts.views',
	#url("^accounts/(?P<person>[\w\W]+)/$", login_required(myaccount), name="myaccount"),
	
	#(r'^accounts/(?P<person>[\w\W]+)/$','myaccount', {'template_name': 'registration/my_account.html'},'myaccount'),
	(r'^register/$', 'register', {'template_name': 'registration/register.html' }, 'register'),	
	(r'^login/$', 'login', {'template_name': 'registration/login.html' }, 'login'),	
	(r'^logout/$', 'logout_user', {'template_name': 'registration/login.html' }, 'logout_user'),	
	#(r'^(?P<username>[\w\W]+)/$','myaccount', {'template_name': 'registration/my_account.html'}, 'myaccount'),
	(r'^my_account/$', 'my_account', {'template_name': 'registration/my_account.html'}, 'my_account'),
)

#urlpatterns += patterns('django.contrib.auth.views',
#	(r'^login/$', 'login', {'template_name': 'registration/login.html'}, 'login'),	
#)
# urlpatterns += patterns('django.contrib.auth.views',
	# (r'^login/$', 'login', {'template_name': 'registration/login.html'}, 'login'),
	
# )

#urlpatterns += patterns('tenthings.aboutme.views',	
	#(r'^(?P<person>[\w\W]+)/$','index'),
#	#(r'^hats/(?P<cat_name>[\w\W]+)/$','category'),
#	#url("^accounts/(?P<person>[\w\W]+)/$", login_required(myaccount), name="myaccount"),
#)

# 'SSL': settings.ENABLE_SSL


