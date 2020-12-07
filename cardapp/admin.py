from django.contrib import admin
from .models import *
from embed_video.admin import AdminVideoMixin
# Register your models here.
@admin.register(CreateLink)
class CreateLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'choose', 'order',)
    list_filter = ('choose',)
    search_fields = ('name',)

admin.site.register(CreateBlock)
admin.site.register(CreateFaq)
admin.site.register(TableCategory)
admin.site.register(TableItems)
admin.site.register(AddImage)
admin.site.register(CardProfile)
admin.site.register(Background)


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(YoutubeVideo, MyModelAdmin)
