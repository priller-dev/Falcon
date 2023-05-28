from django.urls import path
from apps.users.views import ( # noqa
    # FBV
    forgot, login_page,
    logout_page, register,
    reset,
    # CBV
    LoginPage
)

authentication = [
    path('forgot', forgot, name='forgot'),
    # path('login', login_page, name='login'),
    path('login', LoginPage.as_view(), name='login'),
    path('logout', logout_page, name='logout'),
    path('register', register, name='register'),
    path('reset-password/<str:user_id>/<str:token>', reset, name='reset'),
]


urlpatterns = authentication[:]
