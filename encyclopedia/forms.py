from django import forms

class Entryform(forms.Form):
    head = forms.CharField(label='Enter page title')
    body = forms.CharField(label='Enter page markdown content', widget=forms.Textarea)
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
