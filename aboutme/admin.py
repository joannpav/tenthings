from tenthings.aboutme.models import Person
from tenthings.aboutme.models import Thing
from django.contrib import admin

#class HatAdmin(admin.ModelAdmin):
	#list_display = ['ASIN', 'name']
	
#class ChoiceAdmin(admin.ModelAdmin):
#	radio_fields = {"group": admin.VERTICAL}

	
admin.site.register(Person)
admin.site.register(Thing)

