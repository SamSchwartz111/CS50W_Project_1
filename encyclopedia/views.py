from django.shortcuts import render

from . import util

from markdown2 import Markdown

from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from encyclopedia.forms import Entryform

import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    entryTitle = entry
    get = util.get_entry(entry)
    if get is None:
        return render(request, 'encyclopedia/404.html', {
            'title': entryTitle
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            'entry': markdowner.convert(get),
            'title': entryTitle
        })

def newEntry(request):
    form = Entryform()
    if request.method == 'POST':
        form = Entryform(request.POST)
        if form.is_valid():
            head = form.cleaned_data['head']
            body = form.cleaned_data['body']
            if (util.get_entry(head) is None or form.cleaned_data['edit'] is True):
                util.save_entry(head, body)
                return HttpResponseRedirect(reverse('entry', kwargs={'entry': head}))
            else:
                return render(request, 'encyclopedia/newEntry.html', {
                    'form': form,
                    'exists': True,
                    'entry': head,
                })
    return render(request, 'encyclopedia/newEntry.html', {
        'form': form
    })

def rand(request):
    list = util.list_entries()
    rand = random.choice(list)
    return HttpResponseRedirect(reverse('entry', kwargs={'entry': rand}))

def edit(request, entry):
    title = util.get_entry(entry)
    if title is None:
        return render(request, 'encyclopedia/404.html', {
            'title': title
        })
    else:
        form = Entryform()
        form.fields['head'].initial = entry
        form.fields['head'].widget = forms.HiddenInput()
        form.fields['body'].initial = title
        form.fields['edit'].initial = True
        return render(request, 'encyclopedia/newEntry.html', {
            'form': form,
            'edit': form.fields['edit'].initial,
            'title': form.fields['head'].initial,
            'entry': form.fields['body'].initial
        })

def search(request):
    value = request.GET.get('q', '')
    if util.get_entry(value) is not None:
        return HttpResponseRedirect(reverse('entry', kwargs={'entry': value}))
    else:
        subEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subEntries.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": subEntries,
            "search": True,
            "value": value
        })
