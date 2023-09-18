from django.contrib import admin
from .models import MyClass,  EnrolledUser
# Register your models here.
class MyClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_descriptor', 'class_name', 'teacher')
admin.site.register(MyClass, MyClassAdmin)
admin.site.register(EnrolledUser)