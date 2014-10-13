from django.db import models
import datetime
from thumbs import ImageWithThumbsField
from PIL import Image, ImageFile
import pdb
from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=100, null = False)
	username = models.ForeignKey(User)
	image_mimetype = models.TextField(blank = True, null = True)
	#avatar = models.ImageField(upload_to="site_media/images/", max_length=150, help_text="Upload a profile picture", null=True)
	#thumbnail = models.ImageField(upload_to='site_media/images/profile_thumb', blank=True, null=True, editable=False)
	#thumb_photo = ImageWithThumbsField(upload_to='site_media/images', sizes=(125,125))
	#photo = ImageWithThumbsField(upload_to='site_media/images', sizes=(320,240))
	image = models.ImageField(upload_to="site_media/images/", max_length=150, help_text="Upload a profile picture", null=True)
	image_thumb = models.ImageField(upload_to="site_media/images/", max_length=150, null=True)

	def get_person_name(person_id):
		return Person.objects.get(id=person_id)

	def __unicode__(self):
		return self.name
	
	
	# def saveimage(request, string_id):
		# id = int(string_id)
		# entity = Person.objects.filter(id = id)[0]
		# original_mimetype = entity.image_mimetype
		# file = request.FILES.values()[0]
		# extension = file.name.lower().split(".")[-1]
		# if extension == u'jpg':
			# entity.image_mimetype = u'image/jpeg'
		# elif extension == u'swf':
			# entity.image_mimetype = u'application/x-shockwave-flash'
		# else:
			# entity.image_mimetype = u'image/' + extension
		# entity.save()
		# try:        
			# os.rename(settings.MEDIA_ROOT + u'/images/profile/' +
			 # string_id, settings.MEDIA_ROOT + u'/images/profile/' +
			 # string_id + '.old')
		# except OSError:
			# pass		
	
	
class Thing(models.Model):
	thingsAboutMe = models.CharField(max_length=140)
	#person = models.ForeignKey(Person)
	person = models.CharField(max_length=40)
	thing_count = models.IntegerField( null=True)
	person_id = models.IntegerField()
	
	def createInitialThings(request, id, username):
		#pdb.set_trace()
		for i in range(10):
			#t = Thing(thingsAboutMe="Click to Edit", person_id=id, person=username)
			t = Thing(thingsAboutMe="Click to Edit", person_id=id, person=username)
			t.save()
		return t
		
	def __unicode__(self):		
		return self.thingsAboutMe

class Friend(models.Model):
	person = models.ForeignKey(Person) 
	friend = models.ForeignKey(User)
	class Meta:
		unique_together = ('person','friend')
# The comment table holds all comments associeated with a 'thing'
#c = Comment(thing=t.id, comment=request.POST[u'value'],commenter=request.user.id,person=f[0].id)

class Comment(models.Model):
	comment =models.CharField(max_length=1000)
	friend = models.ForeignKey(User) #(Friend)  #this is the person making a comment -> should it be a foreign key?
	thing = models.ForeignKey(Thing)
	person = models.ForeignKey(Person)
	
	def __unicode__(self):
		return self.comment
		
# from http://stackoverflow.com/questions/1164930/image-resizing-with-django
# See Class Photo_Ex for another option
