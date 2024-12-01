from django.shortcuts import render

# Create your views here.
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

# Scopes pour accéder aux fichiers Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Authentifier et obtenir les credentials pour l'API Google Drive
def authenticate_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Fonction pour envoyer un fichier à Google Drive
def upload_to_drive(file_path, file_name):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# Vue pour gérer l'upload via React
class UploadFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        file_path = f'/tmp/{file_obj.name}'
        
        # Sauvegarde temporaire du fichier
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        
        # Envoi à Google Drive
        try:
            file_id = upload_to_drive(file_path, file_obj.name)
            return Response({'message': 'File uploaded successfully', 'file_id': file_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
