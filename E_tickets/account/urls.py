from django.urls import path, include
from .views import *
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/verify/auth/', ProtectedView.as_view(), name='auth-verify'),
]
