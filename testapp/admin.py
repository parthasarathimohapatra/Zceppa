from django.contrib import admin
from .models import *
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display=['customer_id','name','dob','phone','email','password','gender']
    search_fields=('phone','id','email')
admin.site.register(UserProfile,CustomerAdmin)