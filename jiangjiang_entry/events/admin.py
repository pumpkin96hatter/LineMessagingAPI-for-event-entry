from django.contrib import admin
from .models import Line_Name, Event_Type, Entry, Participant, Application_Info, Schedule


from import_export import resources
from import_export.admin import ImportExportMixin

class ApplicationInfoResource(resources.ModelResource):
    class Meta:
        model = Application_Info

class LineNameResource(resources.ModelResource):
    class Meta:
        model = Line_Name

class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant

class EventTypeResource(resources.ModelResource):
    class Meta:
        model = Event_Type
        
        
class ApplicationInfoAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ApplicationInfoResource

class LineNameAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = LineNameResource

class ApplicationInfoInline(admin.TabularInline):
    model = Application_Info

class EventTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    inlines = (ApplicationInfoInline,)
    list_display = ('type_name','event_date')
    resource_class = EventTypeResource

class LineNameInline(admin.TabularInline):
    model = Line_Name

class ParticipantAdmin(ImportExportMixin, admin.ModelAdmin):
    inlines = (LineNameInline,)
    resource_class = ParticipantResource



admin.site.register(Schedule)
admin.site.register(Line_Name, LineNameAdmin)
admin.site.register(Event_Type, EventTypeAdmin)
admin.site.register(Entry)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Application_Info,ApplicationInfoAdmin)
