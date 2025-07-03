from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from account.forms import UserEditForm, ProfileEditForm
from account.forms import UserRegistrationForm, LoginForm
from account.models import Profile


class UserLoginView(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    authentication_form = LoginForm

    def get_success_url(self):
        return reverse_lazy('account:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_register'] = True
        return context


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        Profile.objects.create(user=user)
        return render(
            self.request,
            'account/register_done.html',
            {'new_user': user}
        )


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard.html'
    login_url = 'account:login'


class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'account/edit.html'
    login_url = 'account:login'

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('account:profile')
        else:
            messages.error(request, 'Error updating your profile')
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })
