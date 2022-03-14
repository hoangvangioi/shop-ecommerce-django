from django.db import models
from accounts.models import Account
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,
							unique_for_date='publish')
	author = models.ForeignKey(Account,
							   on_delete=models.CASCADE,
							   related_name='blog_posts')
	body = RichTextUploadingField()
	previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
	next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
							  choices=STATUS_CHOICES,
							  default='draft')
	featured_image = models.ImageField(upload_to='images/%Y/%m/%d/')
	objects = models.Manager()  # The default manager.
	published = PublishedManager()  # Our custom manager.
	post_views = models.IntegerField(default=0, null=True, blank=True)
	tags = TaggableManager()
	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail',
					   args=[self.publish.year,
							 self.publish.month,
							 self.publish.day,
							 self.slug])

		
class Contact(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	name = models.CharField(verbose_name="Name", max_length=100)
	email = models.EmailField(verbose_name="Email", max_length=100, blank=True)
	subject = models.CharField(verbose_name="Subject", max_length=255)
	message = models.TextField(verbose_name="Message")

	def __str__(self):
		return f'{self.name}'

	class Meta:
		verbose_name_plural = 'Contact'
		verbose_name = 'Contact'
		ordering = ["timestamp"]



class Comment(models.Model):
	comment = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(Account, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

	@property
	def children(self):
		return Comment.objects.filter(parent=self).order_by('-created_on').all()

	@property
	def is_parent(self):
		if self.parent is None:
			return True
		return False