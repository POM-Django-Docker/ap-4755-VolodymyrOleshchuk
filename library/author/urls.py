from django.urls import path
from . import views

#Uncomment commented code
#Delete code between "="

urlpatterns = [
    # path("", views.author_list, name="author_list"),
    # path("create/", views.author_create, name="author_create"),
    #=================
    path("", views.authors, name="authors"),
    #=================
    path("delete/<int:author_id>/", views.author_delete, name="author_delete"),
]