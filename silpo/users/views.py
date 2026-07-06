from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserLoginForm, CustomUserRegisterForm
from .utils import save_custom_img
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from users.forms import CustomPasswordResetForm, CustomSetPasswordForm

User = get_user_model()

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

def password_reset_request(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('users:password_reset_done')
        else:
            messages.info(request, 'There are errors in the form')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'password_reset.html', {'form': form})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('users:password_reset_complete')
            else:
                messages.info(request, 'There are errors in the form')
        else:
            form = CustomSetPasswordForm(user)

        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid')
        return render(request, 'password_reset_confirm.html', {'form': None})

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')