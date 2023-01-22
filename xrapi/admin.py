from django.contrib import admin
from .models import Shorturl, Invitation_code
# Register your models here.
admin.site.register(Shorturl)
admin.site.register(Invitation_code)
