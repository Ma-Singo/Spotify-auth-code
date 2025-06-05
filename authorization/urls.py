
from django.urls import path

from .views import  (
 spotify_auth,
spotify_callback,
get_spotify_profile,
get_spotify_player,
)

urlpatterns = [
    path('', spotify_auth, name='spotify_auth'),
    path('callback/', spotify_callback, name='spotify_callback'),
    path('profile/', get_spotify_profile, name='spotify_profile'),
    path('player/', get_spotify_player, name='spotify_player'),
]