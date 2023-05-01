from django.urls import path

from apps.users.views import forgot, login_page, logout_page, register, reset

urlpatterns = [
    path('forgot', forgot, name='forgot'),
    path('login', login_page, name='login'),
    path('logout', logout_page, name='logout'),
    path('register', register, name='register'),
    path('reset-password/<str:user_id>/<str:token>', reset, name='reset'),
]
