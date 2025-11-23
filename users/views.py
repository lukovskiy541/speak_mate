from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm, UserLanguageForm
from .models import UserLanguage

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def add_language(request):
    if request.method == 'POST':
        form = UserLanguageForm(request.POST)
        if form.is_valid():
            user_language = form.save(commit=False)
            user_language.user = request.user
            user_language.save()
            messages.success(request, 'Language added!')
            return redirect('profile')
    else:
        form = UserLanguageForm()
    return render(request, 'users/add_language.html', {'form': form})
