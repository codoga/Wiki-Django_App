from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        existing_entry = util.get_entry(title)
        if existing_entry is not None:
            return render(request, "encyclopedia/create_page.html", {
                "error": "An entry with this title already exists."
            })

        util.save_entry(title, content)
        return redirect('index')

    return render(request, "encyclopedia/create_page.html")

def edit_page(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return HttpResponse("Page not found", status=404)

    if request.method == "POST":
        new_content = request.POST["content"]
        util.save_entry(title, new_content)
        return redirect('entry', title=title)

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": entry_content
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return HttpResponse("Page not found", status=404)

    html_content = markdown2.markdown(entry_content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if matching_entries:
        return render(request, "encyclopedia/index.html", {
            "entries": matching_entries
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": [],
            "message": "No pages found matching your search"
        })
