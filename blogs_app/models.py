from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def get_sentinel_user():
    """get_sentinel_user
    Function for getting or getting user that used in author ForeignKey fields
    if original user is deleted"""
    return get_user_model().objects.get_or_create(username='deleted')[0]


class BlogpostModel(models.Model):
    """Posted blog model
    Fields:
    title -- string, max_length=150
    contents -- string, widget: textfield
    date_created -- date, auto_now_add: True
    author -- related field, model: User, on_delete: SET user 'deleted'

    Meta:
    permissions: can_post_blogpost, can_delete_blogpost"""
    title = models.CharField(_('Title'), max_length=150)
    contents = models.TextField(_('Contents'))
    date_created = models.DateField(_('Creation date'), auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.SET(get_sentinel_user),
                               related_name=_('blogposts'),
                               verbose_name=_('author'))

    class Meta:
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')
        permissions = (
            ('can_post_blogpost', _('can post blogpost')),
            ('can_delete_blogpost', _('can delete blogpost')),
        )

    def __str__(self):
        return self.title


class UploadImageModel(models.Model):
    """Uploaded images model
    Fields:
    blog_post -- related field, model: BlogpostModel, on_delete: CASCADE
    image -- image field, blank: True, null: True"""
    blog_post = models.ForeignKey(BlogpostModel,
                                  on_delete=models.CASCADE,
                                  related_name='image')
    image = models.ImageField(upload_to='files/', blank=True, null=True)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.blog_post


class UploadCSVFile(models.Model):
    """Uploaded CSV file model
    Fields:
    file -- file field"""
    file = models.FileField(upload_to='csv/')

    class Meta:
        verbose_name = _('csv file')
        verbose_name_plural = _('csv files')

    def __str__(self):
        return self.file


class CommentaryModel(models.Model):
    """Posted commentary model
    Fields:
    author -- related field, model: User, on_delete: SET user 'deleted'
    blogpost -- related field, model: BlogpostModel, on_delete: CASCADE
    comment_body -- string, widget: textfield
    date_created -- date, auto_now_add: True
    date_changed -- date, auto_now: True

    Meta:
    permissions: can_post_comment, can_delete_comment"""
    author = models.ForeignKey(User,
                               on_delete=models.SET(get_sentinel_user),
                               related_name=_('commentary'),
                               verbose_name=_('author'))
    blogpost = models.ForeignKey(BlogpostModel,
                                 on_delete=models.CASCADE,
                                 related_name=_('commentary'),
                                 verbose_name=_('blogpost'))
    comment_body = models.TextField(_('body of comment'))
    date_created = models.DateField(_('Creation date'), auto_now_add=True)
    date_changed = models.DateField(_('Change date'), auto_now=True)

    class Meta:
        verbose_name = _('commentary')
        verbose_name_plural = _('commentaries')
        permissions = (
            ('can_post_comment', _('can post comment')),
            ('can_delete_comment', _('can delete comment')),
        )

    def __str__(self):
        return self.comment_body
