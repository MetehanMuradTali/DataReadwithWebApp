from django.db import models
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120, verbose_name="Başlık")
    file = models.FileField(null=True, blank=True)
    user = models.ForeignKey('auth.User', verbose_name='yazar', on_delete=models.CASCADE)

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

class YazarBilgi(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ogretim_turu = models.TextField()

    def __str__(self):
        return str(self.id)



class DanismanBilgi(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    unvan = models.TextField()

    def __str__(self):
        return str(self.id)





class JuriBilgi(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    unvan = models.TextField()

    def __str__(self):
        return str(self.id)

class AnaTablo(models.Model):
    id = models.AutoField(primary_key=True)
    ders_adi  = models.TextField()
    proje_adi = models.TextField()
    yazar_bilgi=models.ForeignKey(YazarBilgi,on_delete=models.CASCADE)
    danisman_bilgi=models.ForeignKey(DanismanBilgi,on_delete=models.CASCADE)
    juri_bilgi=models.ForeignKey(JuriBilgi,on_delete=models.CASCADE)
    teslim_donemi=models.TextField()
    ozet=models.TextField()
    anahtar=models.TextField()

    def __str__(self):
        return str(self.id)