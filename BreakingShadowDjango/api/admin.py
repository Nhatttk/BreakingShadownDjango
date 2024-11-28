from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(Category)
admin.site.register(Expert)
admin.site.register(EmergencyHelp)
admin.site.register(Knowledge)
admin.site.register(Profile)
admin.site.register(PrivateChat)
admin.site.register(Message)