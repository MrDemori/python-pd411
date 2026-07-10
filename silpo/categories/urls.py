from django.urls import path
from . import views

urlpatterns = [
    path("", views.categories, name="categories"),
    path("create/", views.create_category, name="create_category"),
]