from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm

class HomeView(TemplateView):
    template_name = 'home.html'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('account_login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Реєстрацію завершено! Будь ласка, перевірте вашу пошту для підтвердження email.')
        return response

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, 'Ви успішно увійшли!')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Ви вийшли з системи.')
        return super().dispatch(request, *args, **kwargs)

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        messages.success(self.request, 'Інструкції для відновлення паролю надіслано на вашу пошту.')
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

