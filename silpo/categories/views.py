from django.shortcuts import redirect, render
from categories.forms import CategoryForm
from .models import Category

def categories(request):
    categories = Category.objects.all()

    return render(request, "categories.html", {
        "categories": categories
    })

def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form = CategoryForm()

    return render(request, "create_category.html", {
        "form": form
    })
    