from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Post)
admin.site.register(YazarBilgi)
admin.site.register(DanismanBilgi)
admin.site.register(JuriBilgi)
admin.site.register(AnaTablo)