# <!--  aritcle detail template          <a href="{% url 'show_profile_page' post.author.profile.id %}">Profile Page</a>
# -->

from django.shortcuts import render
from django.views import generic
from django.views.generic import DetailView,CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404, render
from .forms import SingUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
from django.contrib.auth.views import PasswordChangeView
from theblog.models import Profile

class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = "registration/create_user_profile_page.html"
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = "registration/edit_profile_page.html"
    fields = ['bio', 'profile_pic', 'website_url', 'faceb_url', 'twitter_url', 'Insta_url', 'pinterest']
    success_url = reverse_lazy('home')


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        # users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context
# class UserRegisterView(generic.CreateView):
#     model = User
#     from_class = UserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')
#     fields = '__all__'

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('home')


class UserRegisterView(generic.CreateView):
    # queryset = User.objects.all()
    form_class = SingUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    # queryset = User.objects.all()
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    # def get_queryset(self):
    #     return User.objects.all()


def logout_view(request):
    print("som tu")
    logout(request)
    return redirect('home')
