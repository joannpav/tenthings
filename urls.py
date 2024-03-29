from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^tenthings/', include('tenthings.foo.urls')),
	#(r'^/', include('tenthings.aboutme.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
	(r'^/', include('tenthings.aboutme.urls')),
	(r'^aboutme/', include('tenthings.aboutme.urls')),
	(r'^/accounts', include('tenthings.accounts.urls')),
)

