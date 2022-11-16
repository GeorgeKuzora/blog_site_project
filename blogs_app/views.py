from csv import reader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from blogs_app.models import BlogpostModel, UploadImageModel, CommentaryModel
from blogs_app.forms import BlogpostForm, CommentaryForm, UploadCSVFileForm, \
                            UploadImageForm
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


class BlogCreationView(View):
    """View for Blog creation page"""

    def get(self, request):
        """GET method for blog creation page

        required can_post_blogpost permission
        required user to be authenticated

        contains forms for blog creation and files(images) upload"""
        user = request.user
        if not user.has_perm("blogs_app.can_post_blogpost"):
             raise PermissionDenied()
        blog_form = BlogpostForm()
        file_form = UploadImageForm()
        return render(request,
                      'blogs_app/create_blog.html',
                      {'blog_form': blog_form,
                       'file_form': file_form}
                      )

    def post(self, request):
        """POST method for blog creation

        required can_post_blogpost permission
        required user to be authenticated

        contains forms for blog creation and files(images) upload
        Checks if BlogpostForm and UploadImageForm is valid
        Creates blogpost
        Uploads images
        Redirects to the blogs-list page"""
        user = request.user
        if not user.has_perm("blogs_app.can_post_blogpost"):
             raise PermissionDenied()
        blog_form = BlogpostForm(request.POST)
        file_form = UploadImageForm(request.POST, request.FILES)
        if blog_form.is_valid() and file_form.is_valid():
            title = blog_form.cleaned_data.get('title')
            contents = blog_form.cleaned_data.get('contents')
            author = user
            current_blog = BlogpostModel.objects.create(title=title,
                                                        contents=contents,
                                                        author=author)
            images = request.FILES.getlist('image')
            for f in images:
                UploadImageModel.objects.create(blog_post=current_blog, image=f)
            return HttpResponseRedirect('/blog')
        return render(request, 'blogs_app/create_blog.html', {'blog_form': blog_form, 'file_form': file_form})


class BlogListView(View):
    """View for Blog list page
    Has only GET method"""
    def get(self, request):
        """GET method for Blog list Page"""
        blog_list = BlogpostModel.objects.all().order_by('-date_created')
        for blog in blog_list:
            blog.contents = blog.contents[:100]
        return render(request, 'blogs_app/blog_list.html', {'blog_list': blog_list})


class BlogDetailView(View):
    """View for the detailed page of the blog
    Contains GET and POST methods"""

    def get(self, request, pk: int):
        """GET method for the detailed page of the blog

        attributes:
        pk: integer number - blog's id number. Used in blog's url

        Contains CommentaryForm for posting comments

        Accessing
        BlogpostModel - blog data
        CommentaryModel - commetntary data
        UploadImageModel - blog's images
        """
        blog_details = BlogpostModel.objects.get(pk=pk)
        current_user = request.user
        images = UploadImageModel.objects.filter(blog_post=blog_details)
        commentary_list = CommentaryModel.objects.filter(blogpost=blog_details)
        form = CommentaryForm()
        return render(request, 'blogs_app/blog_details.html',
                      {'blog_details': blog_details,
                       'pk': pk,
                       'user': current_user,
                       'images': images,
                       'commentary_list': commentary_list,
                       'commentary_form': form}
                      )

    def post(self, request, pk):
        """POST method for the detailed page of the blog
        Required permission can_post_comment

        attributes:
        pk: integer number - blog's id number. Used in blog's url

        Contains CommentaryForm for posting comments

        Accessing
        BlogpostModel - blog data
        CommentaryModel - commetntary data
        UploadImageModel - blog's images

        Validates CommentaryForm
        Posts comment for the blog
        """
        user = request.user
        if not user.has_perm("blogs_app.can_post_comment"):
             raise PermissionDenied()
        blog_details = BlogpostModel.objects.get(pk=pk)
        current_user = request.user
        images = UploadImageModel.objects.filter(blog_post=blog_details)
        commentary_list = CommentaryModel.objects.filter(blogpost=blog_details)
        form = CommentaryForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment_body']
            comment = CommentaryModel.objects.create(author=current_user,
                                                     blogpost=blog_details,
                                                     comment_body=comment_text)
            comment.save()
            return HttpResponseRedirect('/blog/%d' % pk)
        else:
            form.add_error('__all__', _('Error! Please check your comment. \
                                         It should be less than 400 characters.'))
        return render(request, 'blogs_app/blog_details.html',
                      {'blog_details': blog_details,
                       'pk': pk,
                       'user': current_user,
                       'images': images,
                       'commentary_list': commentary_list,
                       'commentary_form': form}
                      )


class UploadCSVFileView(View):
    """View for the page used to mass upload blogpost using CSV file"""

    def get(self, request):
        """GET method for CSV file upload page
        Required permission can_post_blogpost"""
        user = request.user
        if not user.has_perm("blogs_app.can_post_blogpost"):
             raise PermissionDenied()
        upload_form = UploadCSVFileForm()
        return render(request, 'blogs_app/csv_upload.html', {'upload_form': upload_form})

    def post(self, request):
        """POST method for CSV file upload page
        Required permission can_post_blogpost

        Uses UploadCSVFileForm
        Reads CSV file
        Creates blogposts from CSV file's data"""
        user = request.user
        if not user.has_perm("blogs_app.can_post_blogpost"):
             raise PermissionDenied()
        upload_form = UploadCSVFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            blog_file = request.FILES['file'].read()  # upload_form.cleaned_data('file').read()
            # with open(blog_file, newline='') as open_file:
            blog_str = blog_file.decode('utf-8').split('\n')
            for row in blog_str:
                if row:
                    csv_reader = row.split(';')  # reader(row, delimiter=";", quotechar='"')
                    BlogpostModel.objects.create(title=csv_reader[0], contents=csv_reader[1], author=request.user)
            return HttpResponse(_('Blogs have been created successfully'))
        else:
            upload_form = UploadCSVFileForm()
            return render(request, 'blogs_app/csv_upload.html', {'upload_form': upload_form})
