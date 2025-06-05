from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.conf import settings
from urllib.parse import urlencode
import uuid
from django.http import HttpResponse, JsonResponse
import requests
import time


def spotify_auth(request):
    state = str(uuid.uuid4())
    request.session['spotify_auth_state'] = state
    params = {
        "response_type": "code",
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "scope": settings.SPOTIFY_SCOPE,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URL,
        "state": state,
    }
    return redirect(settings.SPOTIFY_AUTH_URL + urlencode(params))

def spotify_callback(request):
    code = request.GET['code']
    state = request.GET['state']

    if not code:
        return JsonResponse({'error': 'Missing Authorization Code'}, status=400)

    # verify state
    #if state != request.session.get('spotify_auth_state'):
    #    return HttpResponse('Invalid state', status=403)

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URL,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
            # 'scope': settings.SPOTIFY_SCOPE,

        }
    )

    if 'error' in response.json():
        return JsonResponse({'error': response.json()['error']}, status=400)

    request.session['spotify_access_token'] = response.json()['access_token']
    request.session['spotify_refresh_token'] = response.json()['refresh_token']
    request.session['spotify_token_expires'] = time.time() + response.json()['expires_in']

    return redirect('spotify_profile')

def get_header(request):
    access_token = request.session['spotify_access_token']
    return {'Authorization': f'Bearer {access_token}'}

def get_spotify_profile(request):
    url = 'https://api.spotify.com/v1/me'
    response = requests.get(url, headers=get_header(request))
    print(response.json())
    return JsonResponse(response.json())


