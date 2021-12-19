from django.db import models
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120, verbose_name="Başlık")
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('post:update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'id': self.id})

    def get_create_url(self):
        return reverse('post:create')
