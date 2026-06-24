from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Author
from .forms import AuthorForm

def is_librarian(user):
    return user.is_authenticated and getattr(user, "role", 0) == 1

#=====================================================================================================
# to restore previous version
# delete functions: authors and author_delete
def authors(request):
    if not request.user.is_authenticated:
        return redirect("home")
    
    authors = Author.get_all()
    
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("authors")
    else:
        form = AuthorForm()
    
    context = {
        "form": form,
        "authors": authors
    }
    
    return render(request, "author/authors.html", context)


def author_delete(request, author_id):
    if not is_librarian(request.user):
        return redirect("home")

    author = get_object_or_404(Author, id=author_id)

    for relation in author._meta.related_objects:
        related_manager = getattr(author, relation.get_accessor_name())
        if related_manager.exists():
            messages.error(request, "Author is attached to a book and cannot be deleted")
            return redirect("authors")

    author.delete()
    return redirect("authors")


#=========================================================================================

# Previous views
# Uncomment this code
# def author_list(request):
#     authors = Author.get_all()
#     return render(request, "author/author_list.html", {"authors": authors})


# def author_create(request):
#     if not is_librarian(request.user):
#         return redirect("home")

#     if request.method == "POST":
#         name = request.POST.get("name")
#         surname = request.POST.get("surname")
#         patronymic = request.POST.get("patronymic")

#         if name and surname and patronymic:
#             Author.create(name=name, surname=surname, patronymic=patronymic)
#             return redirect("author_list")

#         messages.error(request, "All fields are required")

#     return render(request, "author/author_create.html")


# def author_delete(request, author_id):
#     if not is_librarian(request.user):
#         return redirect("home")

#     author = get_object_or_404(Author, id=author_id)

#     for relation in author._meta.related_objects:
#         related_manager = getattr(author, relation.get_accessor_name())
#         if related_manager.exists():
#             messages.error(request, "Author is attached to a book and cannot be deleted")
#             return redirect("author_list")

#     author.delete()
#     return redirect("author_list")