from django.contrib import admin
from task.models import Company,ChunkedUpload
# Register your models here.

admin.site.register(Company)
admin.site.register(ChunkedUpload)