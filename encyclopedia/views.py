from django.shortcuts import render
import markdown
from . import util
import random

def convert(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    h_content = convert(title)
    if h_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This title does not exist try other"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": h_content
        })
    

def search(request):
    if request.method == "POST":
        content = request.POST['q']
        h_content = convert(content)
        if h_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": content,
                "content": h_content
            })
        else:
            entries = util.list_entries()
            recommandation = []
            for entry in entries:
                if content.lower() in entry.lower():
                    recommandation.append(entry)
            return render(request, "encyclopedia/search.html",{
                "recommandation": recommandation
            })
        

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new page.html")
    else:
        new_title = request.POST['title']
        new_content = request.POST['content']
        exist_title = util.get_entry(new_title)
        if exist_title is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "This title already exists"
            })
        else:
            util.save_entry(new_title, new_content)
            h_content = convert(new_title)
            return render(request, "encyclopedia/entry.html", {
                "title": new_title,
                "content": h_content
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        h_content = convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": h_content
        }) 
    
def rand(request):
    title = util.list_entries()
    rand_title = random.choice(title)
    h_content = convert(rand_title)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_title,
        "content": h_content
    })


