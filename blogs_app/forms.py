from django import forms
from django.utils.translation import gettext_lazy as _


class BlogpostForm(forms.Form):
    title = forms.CharField(label=_("Blog's title"), max_length=300)
    contents = forms.CharField(widget=forms.Textarea,
                               label=_('Blogpost contents'),
                               )


class UploadImageForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                             required=False,
                             label=_('Image'))


class UploadCSVFileForm(forms.Form):
    file = forms.FileField(label=_('CSV file'))


class CommentaryForm(forms.Form):
    comment_body = forms.CharField(max_length=400,
                                   widget=forms.Textarea,
                                   label=_('Body of comment'))
