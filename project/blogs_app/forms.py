from django import forms


class BlogpostForm(forms.Form):
    title = forms.CharField()
    contents = forms.CharField(widget=forms.Textarea)


class UploadImageForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class UploadCSVFileForm(forms.Form):
    file = forms.FileField()
