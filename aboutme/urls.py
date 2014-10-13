from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
)

#urlpatterns += patterns('',
#	(r'^inplaceeditform/', include('inplaceeditform.urls')),
#)

urlpatterns += patterns('tenthings.aboutme.views',
	#(r'^(?P<thing_id>\d+)/$','saveChange'),
	#(r'^login/','login'),	
	#(r'^create_user/','create_user'),	
	(r'^save_comment/','save_comment'),
	(r'^delete_comment/','delete_comment'),			
	(r'^save/','save'),
	(r'^addfriend/(\d+)','addfriend'),	
	(r'^searchpage/','searchpage'),			
	(r'^search/','search'),			
	(r'^saveimage/(\d+)', 'saveimage'),
	(r'^accounts/',include('accounts.urls')),
	(r'^accounts/',include('django.contrib.auth.urls')),
	(r'^(?P<person>[\w\W]+)/$','myaccount'),
	
)

urlpatterns += patterns('tenthings.accounts.views',
	#(r'^login/$','login'),
	(r'^$','register'),
)

if settings.DEBUG: urlpatterns += patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root':     settings.MEDIA_ROOT}), 
	(r'^site_media/(?P<category_id>.*)$', 'django.views.static.serve',
	{'document_root':     settings.MEDIA_ROOT}),
) 