from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            return redirect('homepage')
        else:
            messages.info(request, 'Помилка реєстрації')
    else:
        form = CustomUserForm()
    return render(request, 'register.html', {'form': form})