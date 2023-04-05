from django.contrib import admin

from .models import RequestDocument
from django_summernote.admin import SummernoteModelAdmin

#class PostAdmin(SummernoteModelAdmin):
#    summernote_fields = ('body',)
#    list_display = ['title', 'date_created', 'date_update']

admin.site.register(RequestDocument)
