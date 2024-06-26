from django.urls import path
from .views import UserRegisterView, logout_view, UserEditView
from .views import PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout_view'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('<int:uid>/password/', PasswordsChangeView .as_view(template_name='registration/change-password.html')),
    path('<int:pk>/profile', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile/page', EditProfilePageView.as_view(), name='EditProfilePageView'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='CreateProfilePageView'),
]
