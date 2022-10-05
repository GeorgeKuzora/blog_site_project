from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class BlogpostModel(models.Model):
    title = models.CharField(_('Title'), max_length=150)
    contents = models.TextField(_('Contents'))
    date_created = models.DateField(_('Creation date'), auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_('Author'), )

    class Meta:
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')

    def __str__(self):
        return self.title


class UploadImageModel(models.Model):
    blog_post = models.ForeignKey(BlogpostModel, on_delete=models.CASCADE, related_name='Файлы')
    image = models.ImageField(upload_to='files/', blank=True, null=True)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.blog_post


class UploadCSVFile(models.Model):
    file = models.FileField(upload_to='csv/')

    class Meta:
        verbose_name = _('csv file')
        verbose_name_plural = _('csv files')

    def __str__(self):
        return self.file
