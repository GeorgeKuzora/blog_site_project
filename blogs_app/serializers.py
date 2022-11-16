# Сериализаторы нужны для преобразования данных из базы данных
# в подходящий формат для передачи по сети
from rest_framework import serializers
from blogs_app.models import BlogpostModel, CommentaryModel, UploadImageModel
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Class for serializing User model
    """
    blogposts = serializers.HyperlinkedIdentityField(many=True,
                                                     view_name='blogpost-detail',
                                                     read_only=True,
                                                     )
    commentary = serializers.HyperlinkedIdentityField(many=True,
                                                    view_name='comment-detail',
                                                    read_only=True,
                                                    )
    detailed_view = serializers.HyperlinkedIdentityField(source='username',
                                                  view_name='user-detail',
                                                  read_only=True,)
    class Meta:
        model = User
        fields = ['id', 'username', 'blogposts', 'commentary', 'detailed_view']


class BlogpostSerializer(serializers.ModelSerializer):
    """
    Class for serializing BlogpostModel
    """
    author = serializers.HyperlinkedRelatedField(view_name='user-detail',
                                                 read_only=True)
    commentary = serializers.HyperlinkedIdentityField(many=True,
                                                    view_name='comment-detail',
                                                    read_only=True)
    detailed_view = serializers.HyperlinkedIdentityField(source='title',
                                                  view_name='blogpost-detail',
                                                  read_only=True,)
    uploaded_images = serializers.HyperlinkedIdentityField(source='image',
                                                  view_name='uploadimage-detail',
                                                  read_only=True,
                                                  many=True)

    class Meta:
        model = BlogpostModel
        fields = ['title',
                  'contents',
                  'date_created',
                  'author',
                  'commentary',
                  'detailed_view',
                  'uploaded_images']


class CommentSerializer(serializers.ModelSerializer):
    """
    Class for serializing CommentaryModel
    """
    author = serializers.HyperlinkedIdentityField(source='author.username',
                                                    view_name='user-detail',
                                                    read_only=True)
    blogpost = serializers.HyperlinkedRelatedField(queryset=BlogpostModel.objects.all(),
                                                    view_name='blogpost-detail',
                                                    )
    detailed_view = serializers.HyperlinkedIdentityField(
                                                  view_name='comment-detail',
                                                  read_only=True,)

    class Meta:
        model = CommentaryModel
        fields = ['author', 'blogpost', 'comment_body', 'detailed_view']


class UploadImageSerializer(serializers.ModelSerializer):
    """
    Class for serializing UploadImageModel
    """
    blog_post = serializers.HyperlinkedRelatedField(queryset=BlogpostModel.objects.all(),
                                                     view_name='blogpost-detail',
                                                     )
    detailed_view = serializers.HyperlinkedIdentityField(source='image',
                                                  view_name='uploadimage-detail',
                                                  read_only=True,
                                                  )
    class Meta:
        model = UploadImageModel
        fields = ['blog_post', 'image', 'detailed_view']
