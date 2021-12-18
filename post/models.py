from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120,verbose_name="Başlık")
    file= models.FileField(null=True,blank=True)

    def __str__(self):
        return self.title