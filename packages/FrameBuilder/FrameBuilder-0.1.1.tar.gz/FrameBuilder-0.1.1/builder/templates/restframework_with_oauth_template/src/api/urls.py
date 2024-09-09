from django.urls import path, include


urlpatterns = [
    path('oauth/', include('api.oauth.urls')),
    path('users/', include('api.users.urls')),
]
