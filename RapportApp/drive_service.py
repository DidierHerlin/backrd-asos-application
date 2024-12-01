from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload, HttpError
import logging

# Configuration des scopes et fichier de service
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets'
]
SERVICE_ACCOUNT_FILE = 'RapportApp/service_account.json'
PARENT_FOLDER_ID = "1rGwcYFHbOjTlDotGI6j5L5gjBD8KJuwQ"

# Authentification avec désactivation du cache
def authenticate():
    """Authentifie et retourne les crédentials Google API."""
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return creds
    except Exception as e:
        logging.error(f"Erreur d'authentification : {e}")
        return None

def build_service(api_name, api_version, creds):
    """Construit un service Google API avec le cache désactivé pour éviter les avertissements."""
    return build(api_name, api_version, credentials=creds, cache_discovery=False)

# Téléchargement du fichier sur Google Drive
def upload_file(file_path, username):
    """Télécharge un fichier sur Google Drive et retourne l'ID du fichier Google Sheets mis à jour."""
    creds = authenticate()
    if not creds:
        return None  # Authentification échouée

    try:
        drive_service = build_service('drive', 'v3', creds)
        file_metadata = {
            'name': f'{username}_{file_path.split("/")[-1]}',
            'parents': [PARENT_FOLDER_ID]
        }
        media = MediaFileUpload(file_path, mimetype='application/pdf')
        
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = file.get('id')
        file_name = file_metadata['name']
        print(f"Fichier téléchargé avec succès, ID : {file_id}")

        return update_google_sheet(username, file_name, creds)

    except HttpError as error:
        logging.error(f"Erreur lors de l'upload sur Google Drive : {error}")
        return None

# Mise à jour de Google Sheets
def update_google_sheet(username, file_name, creds):
    """Mise à jour Google Sheets avec le nom d'utilisateur et le nom du fichier."""
    try:
        sheets_service = build_service('sheets', 'v4', creds)
        spreadsheet_id = find_or_create_spreadsheet(sheets_service, username)

        data = [[username, file_name]]
        populate_sheet(spreadsheet_id, sheets_service, data)

        return spreadsheet_id

    except HttpError as error:
        logging.error(f"Erreur lors de l'accès à Google Sheets : {error}")
        return None

# Recherche ou création de la feuille de calcul
def find_or_create_spreadsheet(sheets_service, username):
    """Vérifie l'existence de la feuille de calcul ou en crée une nouvelle."""
    spreadsheet_id = f"{username}"
    try:
        sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        return spreadsheet_id

    except HttpError as error:
        if error.resp.status == 404:
            sheet_metadata = {
                'properties': {
                    'title': spreadsheet_id
                }
            }
            sheet = sheets_service.spreadsheets().create(body=sheet_metadata, fields='spreadsheetId').execute()
            spreadsheet_id = sheet.get('spreadsheetId')
            print(f"Google Sheets créé avec succès, ID : {spreadsheet_id}")
            return spreadsheet_id
        else:
            logging.error(f"Erreur lors de la recherche de la feuille : {error}")
            return None

# Ajout de données à Google Sheets
def populate_sheet(spreadsheet_id, sheets_service, data):
    """Ajoute des données à une feuille de calcul existante."""
    try:
        range_name = "Sheet1"
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name
        ).execute()
        
        start_row = len(result.get('values', [])) + 1
        body = {'values': data}
        
        result = sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"Sheet1!A{start_row}",
            valueInputOption="RAW",
            body=body
        ).execute()
        
        print(f"{result.get('updates').get('updatedCells')} cellules mises à jour.")

    except HttpError as error:
        logging.error(f"Erreur lors de l'ajout des données : {error}")
