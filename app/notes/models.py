from django.contrib import auth
from django.contrib.auth.models import User, AbstractUser, UserManager
from django.db import models
from django.urls import reverse


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, db_index=True)
    content = models.TextField()
    icon = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_url(self, template):
        return reverse(template, kwargs={'username': self.user.username, 'slug': self.slug})

    def get_absolute_url(self):
        return self.get_url('show_note')

    def get_update_url(self):
        return self.get_url('update_note')

    def get_delete_url(self):
        return self.get_url('delete_note')

    class Meta:
        ordering = ['-time_updated']


class Folder(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, db_index=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_url(self, template):
        return reverse(template, kwargs={'username': self.user.username, 'slug': self.slug})

    def get_absolute_url(self):
        return self.get_url('show_folder')

    def get_delete_url(self):
        return self.get_url('delete_folder')

    class Meta:
        ordering = ['-time_updated']
