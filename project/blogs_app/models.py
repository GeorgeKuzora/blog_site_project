from django.db import models
from django.contrib.auth.models import User


class BlogpostModel(models.Model):
    title = models.CharField('Заголовок', max_length=150)
    contents = models.TextField('Содержание')
    date_created = models.DateField('Дата создания', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Автор', )

    def __str__(self):
        return self.title


class UploadImageModel(models.Model):
    blog_post = models.ForeignKey(BlogpostModel, on_delete=models.CASCADE, related_name='Файлы')
    image = models.ImageField(upload_to='files/', blank=True, null=True)

    def __str__(self):
        return self.blog_post


class UploadCSVFile(models.Model):
    file = models.FileField(upload_to='csv/')

    def __str__(self):
        return self.file
