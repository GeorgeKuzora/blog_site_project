from django.urls import path, include
from . views import BlogCreationView, BlogDetailView, BlogListView, UploadCSVFileView
from . api import UploadImageViewSet, UserViewSet, BlogpostViewSet, CommentViewSet
    # UserDetailApi, UsersListApi, \
    # BlogpostDetailApi, BlogpostsListApi, api_root, \
    # CommentDetailApi, CommentListApi, \
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user')
router.register(r'blogs', BlogpostViewSet, basename='blogpost')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'uploadimages', UploadImageViewSet, basename='uploadimage')
urlpatterns = [
        path('create_blog/', BlogCreationView.as_view(), name='create_blog'),
        path('blog/', BlogListView.as_view(), name='blog_list'),
        path('blog/<int:pk>', BlogDetailView.as_view(), name='blog_details'),
        path('create_blog/csv', UploadCSVFileView.as_view(), name='csv_file_upload'),
        # path('api/blogs', BlogpostsListApi.as_view(), name='blogpost-list'),
        # path('api/blog_detail/<int:pk>', BlogpostDetailApi.as_view(), name='blogpost-detail'),
        # path('api/users', UsersListApi.as_view(), name='user-list'),
        # path('api/user_detail/<int:pk>', UserDetailApi.as_view(), name='user-detail'),
        # path('api/comments', CommentListApi.as_view(), name='comment-list'),
        # path('api/comment_detail/<int:pk>', CommentDetailApi.as_view(), name='comment-detail'),
        path('api/', include(router.urls)),
        # path('api/', api_root),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns)
