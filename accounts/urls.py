from django.urls import path
from .views import user_login, user_logout, user_profile, user_register, ProfileEditView, admin_panel
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView

urlpatterns = [
    path('login/', user_login, name = 'login'),
    path('logout/', user_logout, name= 'logout'),
    path('profile/', user_profile, name='profile'),
    path('password-change/', PasswordChangeView.as_view(), name= 'password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password_reset'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('signup/', user_register, name='user_register'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('adminpanel/', admin_panel, name='admin_panel')
]
