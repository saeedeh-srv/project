from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, UserRegisterForm, UserProfileUpdateForm
from django.contrib import messages
from django.views.generic import View, UpdateView
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import os
from django.conf import settings

class RegisterUser(View):
    form_class = UserRegisterForm
    template_name = 'Accounts/register.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'form': self.form_class})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = User.objects.create_user(username=data['username'],
                                            email=data['email'],
                                            last_name=data['last_name'],
                                            first_name=data['first_name'],
                                            password=data['password_1'])
            Profile.objects.create(
                user=user,
                phone=data['phone_number'],
            )
            login(self.request, user)
            messages.success(self.request, f"welcome", 'success')
            return redirect('accounts:user_profile')
        return render(self.request, self.template_name, {"form": form})


class LoginUser(auth_views.LoginView):
    form_class = UserLoginForm
    template_name = 'Accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:user_profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(172800)  # expired after 2 days
        else:
            self.request.session.set_expiry(0)  # expired after user close the browser
        self.request.session.modified = True

        messages.success(self.request, f"welcome", 'success')
        return super(LoginUser, self).form_valid(form)




class ProfileUser(View):
    def get(self, *args, **kwargs):
        request = self.request
        profile = get_object_or_404(Profile, user=request.user)
        context = {
            'profile': profile
        }
        return render(request, 'Accounts/profile.html', context)



class LogoutUser(View):

    def get(self, request):
        logout(request)
        messages.success(self.request, f"We Hope See You Again !!", 'success')
        return redirect('accounts:user_login')


class ChangePasswordUser(SuccessMessageMixin, PasswordChangeView):
    template_name = 'Accounts/change_password.html'
    success_message = 'Password was changed successfully'
    success_url = reverse_lazy('accounts:user_profile')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserProfileUpdateForm
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('accounts:user_profile')  # Redirect after successful update

    def get_form_kwargs(self):
        """Pass the current user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self, queryset=None):
        """Return the profile of the logged-in user."""
        return self.request.user.profile

    def form_valid(self, form):
        """If the form is valid, save both the user and profile."""
        profile = self.get_object()

        # Check if the old image exists and needs to be removed
        old_image = profile.image
        new_image = form.cleaned_data.get('image')

        # Remove the old image if a new one is uploaded
        if old_image and new_image:
            old_image_path = old_image.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

                # Save the profile instance
        return super().form_valid(form)


    def get_success_url(self):
        messages.success(self.request, 'Profile updated successfully!')
        return reverse('accounts:user_profile')