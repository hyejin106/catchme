from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ExifTags


class Catching(models.Model):
	image = models.ImageField(upload_to='catching_image/', null=True)
	comment = models.TextField(null=True)
	like_count = models.IntegerField(default=0)
	singo_count = models.IntegerField(default=0)
	chatting_count = models.IntegerField(default=0)
	is_in_pocket = models.BooleanField(default=False)
	is_recognized = models.BooleanField(default=True)
	confidence = models.IntegerField(default=0)
	registered_time = models.DateTimeField(auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)
	senior = models.ForeignKey('Senior', null=True)
	profile = models.ForeignKey('Profile')

	def save(self, force_insert=False, force_update=False, using=None): 
		for field in self._meta.fields: 
			if field.name == 'image': 
				try: 
					image=Image.open(self.image)

					for orientation in ExifTags.TAGS.keys():
						if ExifTags.TAGS[orientation]=='Orientation':
							break
 
					exif = dict(image._getexif().items()) 

					if exif[orientation] == 3:
						image=image.rotate(180, expand=True)
					elif exif[orientation] == 6:
						image=image.rotate(270, expand=True)					
					elif exif[orientation] == 8: 
						image=image.rotate(90, expand=True)
					
					image.save(self.image.path, 'JPEG')
 
				except (AttributeError, KeyError, IndexError):
					pass

			super(Catching, self).save() 


class Senior(models.Model):
    name = models.CharField(max_length=15)
    image = models.ImageField(upload_to='senior_image/', null=True)
    student_id = models.IntegerField(null=True)
    like_count = models.IntegerField(default=0)
    caught_count = models.IntegerField(default=0)
    registered_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)
 
    def save(self, force_insert=False, force_update=False, using=None):
		for field in self._meta.fields:
			if field.name == 'image':
				try:
					image=Image.open(self.image)

					for orientation in ExifTags.TAGS.keys():
						if ExifTags.TAGS[orientation]=='Orientation':
							break

					exif = dict(image._getexif().items())

					if exif[orientation] == 3:
						image=image.rotate(180, expand=True)
					elif exif[orientation] == 6:
						image=image.rotate(270, expand=True)
					elif exif[orientation] == 8:
						image=image.rotate(90, expand=True)

					image.save(self.image.path, 'JPEG')

				except (AttributeError, KeyError, IndexError):
					pass
        
			super(Senior, self).save()


class Profile(models.Model):
    user = models.OneToOneField(User)
    is_freshman = models.BooleanField(default=True)
    catching_count = models.IntegerField(default=0)
    registered_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)
 

class Chatting(models.Model):
    chat = models.TextField(null=False)
    profile = models.ForeignKey('Profile', null=True)
    catching = models.ForeignKey('Catching', null=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)
 

class Like(models.Model):
    profile = models.ForeignKey('Profile')
    catching = models.ForeignKey('Catching')
    registered_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)
 

class Singo(models.Model):
    profile = models.ForeignKey('Profile')
    catching = models.ForeignKey('Catching')
    registered_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)
 
