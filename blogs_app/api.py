from rest_framework import permissions, viewsets
from blogs_app.models import BlogpostModel, CommentaryModel, UploadImageModel
from django.contrib.auth.models import User
from blogs_app.serializers import BlogpostSerializer, UploadImageSerializer, UserSerializer, CommentSerializer
from blogs_app.permissions import IsAuthorOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'retrieve' actions for User model
    """
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer


class BlogpostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list' and 'retrieve' actions for Blogpost model
    """
    queryset = BlogpostModel.objects.order_by('id')
    serializer_class = BlogpostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list' and 'retrieve' actions for Commentary model
    """
    queryset = CommentaryModel.objects.order_by('id')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UploadImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list' and 'retrieve' actions for UploadImage model
    """
    queryset = UploadImageModel.objects.order_by('id')
    serializer_class = UploadImageSerializer
