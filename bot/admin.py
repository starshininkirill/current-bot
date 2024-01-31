from django.contrib import admin
from .models import Users, Welcome, Config

admin.site.register(Config)
admin.site.register(Users)
admin.site.register(Welcome)
