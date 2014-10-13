#!/usr/bin/python
import os, sys

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))
import site
site.addsitedir('/home/hatzillion/modules/django-inplaceedit-0.55')
site.addsitedir('/home/hatzillion/modules/django_inplaceedit-0.55-py2.6.egg')
site.addsitedir('/home/hatzillion/modules/')

_PROJECT_NAME = _PROJECT_DIR.split('/')[-1]
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % _PROJECT_NAME

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
