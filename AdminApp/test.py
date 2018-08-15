from __future__ import print_function
from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from apiclient.http import MediaInMemoryUpload
from oauth2client import file as oauth_file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'
print("Imported")

def main():
    """Shows basic usage of the Drive v3 API.

    Prints the names and ids of the first 10 files the user has access to.
    """
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    """
    get file by id
    print(service.files().get(fileId='0B8VthSNk0FTid0JUeUhIeUVBT1U',fields='webContentLink').execute())
    """
    print(service.files().get(fileId='0B8VthSNk0FTid0JUeUhIeUVBT1U',fields='webContentLink').execute())


store = oauth_file.Storage('AdminApp/token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('AdminApp/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))
print(service)