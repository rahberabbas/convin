from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework.response import Response

class GoogleCalendarInitView(View):
    def get(self, request):
        scopes = ['https://www.googleapis.com/auth/calendar.events']

        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRET_FILE, #( Google Client Secret json file path in settings.py)
            scopes=scopes
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        return HttpResponseRedirect(authorization_url)
    
    
class GoogleCalendarRedirectView(View):
    def get(self, request):
        authorization_code = request.GET.get('code')

        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly']
        )

        flow.fetch_token(authorization_response=request.build_absolute_uri())

        service = build('calendar', 'v3', credentials=flow.credentials)

        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        return Response(events, safe=False)