from django.contrib import admin

# Register your models here.
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user_id', 'title', 'file']


class YazarAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'ogretim_turu']


class DanismanAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'unvan']


class JuriAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'unvan']


class AnaTabloAdmin(admin.ModelAdmin):
    list_display = ['id', 'ders_adi', 'proje_adi','teslim_donemi', 'yazar_bilgi_id', 'juri_bilgi_id', 'danisman_bilgi_id', 'anahtar']
    list_filter = ['yazar_bilgi_id','ders_adi','proje_adi','anahtar','teslim_donemi']


admin.site.register(Post, PostAdmin)
admin.site.register(YazarBilgi, YazarAdmin)
admin.site.register(DanismanBilgi, DanismanAdmin)
admin.site.register(JuriBilgi, JuriAdmin)
admin.site.register(AnaTablo, AnaTabloAdmin)
