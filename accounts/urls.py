from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    # path('signup/done/', views.SignupDone.as_view(), name='signup_done'),
    # path('signup/complete/<token>/', views.SignupComplete.as_view, name='signup_complete'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('profile/edit/<int:pk>', views.UserEditView.as_view(), name='profile_edit'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('password_change/', views.Password.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordDone.as_view(), name='password_change_done'),
    path('password_reset/', views.RePassword.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.RePasswordConfirm.as_view(), name='password_reset_confirm'),
    path('delete/<int:pk>', views.UserDelete.as_view(), name='user_delete'),
]