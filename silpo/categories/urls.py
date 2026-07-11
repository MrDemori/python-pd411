from django.urls import path
from . import views

app_name = "categories"

urlpatterns = [
    path("", views.categories, name="list"),
    path("create/", views.create_category, name="create"),
    path("<int:pk>/edit/", views.edit_category, name="edit"),
    path("<int:pk>/delete/", views.delete_category, name="delete")
]