from django.contrib import admin
from .models import Event_Type, Entry, Application_Log, Application_Info
#  imoport Event_Date,


class ApplicationLogInline(admin.TabularInline):
    model = Application_Log

class ApplicationInfoAdmin(admin.ModelAdmin):
    inlines = (ApplicationLogInline,)
    list_display = ('participant', 'applied_at')


# Register your models here.
admin.site.register(Event_Type)
admin.site.register(Entry)
admin.site.register(Application_Info, ApplicationInfoAdmin)
admin.site.register(Application_Log)
