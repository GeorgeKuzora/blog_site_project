from django.urls import path
from . views import BlogCreationView, BlogDetailView, BlogListView, UploadCSVFileView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('create_blog/', BlogCreationView.as_view(), name='create_blog'),
        path('blog/', BlogListView.as_view(), name='blog_list'),
        path('blog/<int:pk>', BlogDetailView.as_view(), name='blog_details'),
        path('create_blog/csv', UploadCSVFileView.as_view(), name='csv_file_upload'),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
