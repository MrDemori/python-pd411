from django.shortcuts import redirect, render, get_object_or_404

from products.forms import ProductForm
from products.models import ProductImage
from .forms import CategoryForm
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
            return redirect("categories:list")
    else:
        form = CategoryForm()

    return render(request, "create_category.html", {
        "form": form
    })
    
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("categories:list")

    return redirect("categories:list")

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():
            form.save()
            return redirect("categories:list")
    else:
        form = CategoryForm(instance=category)

    return render(request, "edit_category.html", {
        "form": form,
        "category": category
    })

def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)

    products = category.products.all()

    return render(
        request,
        "products/products.html",
        {
            "category": category,
            "products": products,
        },
    )

def create_product(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            images = request.FILES.getlist('image')
            for i, image in enumerate(images):
                ProductImage.objects.create(product=product, image=image, priority=i)
            return redirect("categories:products", pk=category.pk)
    else:
        form = ProductForm()
    return render(request, "products/create_product.html",{
        "form": form,
        "category": category
    })