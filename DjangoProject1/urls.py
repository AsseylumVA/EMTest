from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('business/', include('business.urls', namespace='business')),
    path('rbac/', include('rbac.urls', namespace='rbac')),
]
