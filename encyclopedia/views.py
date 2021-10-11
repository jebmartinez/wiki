from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django import forms
from markdown2 import markdown
import random

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="Entry", max_length=50)
    text = forms.CharField(label="Content", widget=forms.Textarea())


def index(request):
    # entry name for edit
    request.session["entry"] = ""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def randompage(request):
    entries = util.list_entries()
    if len(entries)>0:
        random.shuffle(entries)
        response = redirect(f"/wiki/{entries[0]}")
        return response
    else:
        return HttpResponseRedirect(reverse("index"))

def edit2(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            entry = markdown(text)
            request.session["entry"] = title
            return render(request,"encyclopedia/entry.html", {
                "title": title,
                "entry": entry

            })
    else:
        if "entry" not in request.session:
            return HttpResponseRedirect(reverse("index"))
        else:
            title = request.session["entry"]
            text = util.get_entry(title)
            if text == None:
                msg = "Item não encontrado"
                return render(request, "encyclopedia/entryerror.html", {
                    "title": title,
                    "msg": msg
                })
            data = {'title': title, 'text': text}
            form = EntryForm(initial=data)

    return render(request, "encyclopedia/editpage2.html", {
                "form": form
            })

def edit(request):
    if request.POST:
        pagedata = request.POST.dict()
        title = pagedata.get('title')
        text = pagedata.get('text')
        util.save_entry(title, text)
        entry = markdown(text)
        request.session["entry"] = title
        return render(request,"encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })    
    else:
        if "entry" not in request.session:
            return HttpResponseRedirect(reverse("index"))
        else:
            title = request.session["entry"]
            text = util.get_entry(title)
            if text == None:
                msg = "Item não encontrado"
                return render(request, "encyclopedia/entryerror.html", {
                    "title": title,
                    "msg": msg
                })
            return render(request, "encyclopedia/editpage.html", {
                "title": title,
                "content": text
            })


def newpage(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            if util.exists_entry(title):
                msg="Item já existe"
                return render(request, "encyclopedia/entryerror.html", {
                    "title": title,
                    "msg": msg
                })
            else:
                util.save_entry(title, text)
                entry = markdown(text)
                request.session["entry"] = title
                return render(request,"encyclopedia/entry.html", {
                    "title": title,
                    "entry": entry
                })   
    else:
        form = EntryForm() 
    return render(request, "encyclopedia/newpage.html", {
        'form' : form
    })


def search(request):
    if request.GET:
        searchdata = request.GET.dict()
        title = searchdata.get('q')
        text = util.get_entry(title)
        if text == None:
            entries = util.list_entries()
            filtered = [entry for entry in entries if entry.find(title) != -1]
            if len(filtered) > 0:
                return render(request, "encyclopedia/index.html", {
                    "entries": filtered
                })
            else:
                msg = "Nenhum item corresponde aos critérios de pesquisa"
                return render(request, "encyclopedia/entryerror.html", {
                    "title": title,
                    "msg": msg
                })
        else:
            request.session["entry"] = title
            entry = markdown(text)
            return render(request,"encyclopedia/entry.html", {
                "title": title,
                "entry": entry
            })    

def entry(request, title):
    text = util.get_entry(title)
    if text == None:
        msg = "Item não encontrado"
        return render(request, "encyclopedia/entryerror.html", {
            "title": title,
            "msg": msg
        })
    request.session["entry"] = title
    entry = markdown(text)
    return render(request,"encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })
