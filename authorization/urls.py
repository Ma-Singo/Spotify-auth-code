
from django.urls import path

from .views import  (
 spotify_auth,
spotify_callback,
get_spotify_profile
)

urlpatterns = [
    path('', spotify_auth, name='spotify_auth'),
    path('callback/', spotify_callback, name='spotify_callback'),
    path('profile/', get_spotify_profile, name='spotify_profile'),
]