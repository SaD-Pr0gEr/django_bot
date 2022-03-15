from django.urls import path

from accounts.views import login_page, logout_users, signup_page, email_confirm

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_page, name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_users, name='logout'),
    path('email/confirm/<str:email>', email_confirm, name='email_confirm'),
]
