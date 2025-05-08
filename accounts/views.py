from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid

from accounts.models import CustomUser

from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse('moviedb:home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.activation_token = str(uuid.uuid4())
            user.save()
            
            # Envoyer l'email d'activation
            activation_link = request.build_absolute_uri(
                reverse('accounts:activate', args=[user.activation_token])
            )
            send_mail(
                'Activez votre compte',
                f'Cliquez sur ce lien pour activer votre compte: {activation_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Compte créé avec succès! Veuillez vérifier votre email pour activer votre compte.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def activate_account(request, token):
    try:
        user = CustomUser.objects.get(activation_token=token)
        user.is_active = True
        user.activation_token = ''
        user.save()
        messages.success(request, 'Votre compte a été activé avec succès!')
        return redirect('accounts:login')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Le lien d\'activation est invalide!')
        return redirect('accounts:register')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })