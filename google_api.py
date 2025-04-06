import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build


def list_image_links(folder_id):
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    # Load service account info from environment variable
    service_account_info = json.loads(os.environ["GCP_SA_KEY"])
    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )

    service = build("drive", "v3", credentials=creds)

    # Query for image files inside the folder
    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()

    items = results.get("files", [])

    # Convert to direct image download links
    links = [
        f"https://drive.google.com/uc?export=download&id={item['id']}" for item in items
    ]

    return links
