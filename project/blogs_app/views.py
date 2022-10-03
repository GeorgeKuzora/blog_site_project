from csv import reader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from blogs_app.models import BlogpostModel, UploadImageModel
from blogs_app.forms import BlogpostForm, UploadCSVFileForm, UploadImageForm
from django.core.exceptions import PermissionDenied


class BlogCreationView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied()
        blog_form = BlogpostForm()
        file_form = UploadImageForm()
        return render(request, 'blogs_app/create_blog.html', {'blog_form': blog_form, 'file_form': file_form})

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied()
        blog_form = BlogpostForm(request.POST)
        file_form = UploadImageForm(request.POST, request.FILES)
        if blog_form.is_valid() and file_form.is_valid():
            title = blog_form.cleaned_data.get('title')
            contents = blog_form.cleaned_data.get('contents')
            author = user
            current_blog = BlogpostModel.objects.create(title=title, contents=contents, author=author)
            images = request.FILES.getlist('image')
            for f in images:
                UploadImageModel.objects.create(blog_post=current_blog, image=f)
            return HttpResponseRedirect('/blog')
        return render(request, 'blogs_app/create_blog.html', {'blog_form': blog_form, 'file_form': file_form})


class BlogListView(View):
    def get(self, request):
        blog_list = BlogpostModel.objects.all().order_by('-date_created')
        for blog in blog_list:
            blog.contents = blog.contents[:100]
        return render(request, 'blogs_app/blog_list.html', {'blog_list': blog_list})


class BlogDetailView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponse('Для просмотра записи пройдите аутентификацию')
        else:
            blog_details = BlogpostModel.objects.get(pk=pk)
            current_user = request.user
            images = UploadImageModel.objects.filter(blog_post=blog_details)
            return render(request, 'blogs_app/blog_details.html',
                        {'blog_details': blog_details,
                         'pk': pk,
                         'user': current_user,
                         'images': images})


class UploadCSVFileView(View):
    def get(self, request):
        upload_form = UploadCSVFileForm()
        return render(request, 'blogs_app/csv_upload.html', {'upload_form': upload_form})

    def post(self, request):
        upload_form = UploadCSVFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            blog_file = request.FILES['file'].read()  # upload_form.cleaned_data('file').read()
            # with open(blog_file, newline='') as open_file:
            blog_str = blog_file.decode('utf-8').split('\n')
            for row in blog_str:
                if row:
                    csv_reader = row.split(';')  # reader(row, delimiter=";", quotechar='"')
                    BlogpostModel.objects.create(title=csv_reader[0], contents=csv_reader[1], author=request.user)
            return HttpResponse(content='Блоги были успешно созданы')
        else:
            upload_form = UploadCSVFileForm()
            return render(request, 'blogs_app/csv_upload.html', {'upload_form': upload_form})
