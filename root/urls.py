from django.conf import urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.products.client.admin import client_site
from root.exceptions import custom_404, custom_500
from root.settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT, DEBUG
import socket
from django.http import JsonResponse

req_num = 0

def func(request):
    global req_num
    req_num += 1
    return JsonResponse({"request_num": req_num, "HOST": socket.gethostname()})

urlpatterns = [
    path('', func),
    path('admin/', admin.site.urls),
    # path('', include(('apps.products.urls', 'products'), namespace='products')),
    path('auth/',
         include(('apps.users.urls', 'users'), namespace='users')
    ),
    path('client-site/', client_site.urls),
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

urls.handler404 = custom_404
urls.handler500 = custom_500
