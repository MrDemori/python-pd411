from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserLoginForm, CustomUserRegisterForm
from .utils import save_custom_img
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if 'email' in form.cleaned_data:
                    user.username = form.cleaned_data['email']
                if 'image' in request.FILES:
                    image = request.FILES['image']
                    user.image_small = save_custom_img(image, (300, 300), 'small')
                    user.image_medium = save_custom_img(image, (800, 800), 'medium')
                    user.image_large = save_custom_img(image, (1200, 1200), 'large')
                user.save()
                login(request, user)
                return redirect('homepage')
            except Exception as e:
                print(f"Error with saving image: {str(e)}")
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.info(request, 'Error with registration.')
    else:
        form = CustomUserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data = request.POST)
        if form.is_valid():
            user = authenticate(request, 
                                username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('homepage')
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('homepage')
