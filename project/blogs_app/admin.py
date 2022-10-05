from django.contrib import admin
from blogs_app.models import BlogpostModel, UploadImageModel, UploadCSVFile

admin.site.register(BlogpostModel)
admin.site.register(UploadImageModel)
admin.site.register(UploadCSVFile)
