from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/auth.html', {
        'form': form,
        'title': 'Sign In',
        'sign_in': True,
    })

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main_page')
    else:
        form = UserCreationForm()

    return render(request, 'registration/auth.html', {
        'form': form,
        'title': 'Sign Up',
    })

def logout_view(request):
    logout(request)
    return redirect('main_page')