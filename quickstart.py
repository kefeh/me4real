# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import pickle

import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

# the token.pickel file holds the credentials and you need to deploy it to server to be able to
# access your email from the server
TOKEN_PICKLE = f"token.pickle"
CREDENTIALS = f"credentials.json"

SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.upload"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    # client_secrets_file = "client_secret_864246643627-106pb92mqtq6t63jodls8tmhebqr824u.apps.googleusercontent.com.json"
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    # # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()
    # youtube = googleapiclient.discovery.build( credentials=credentials)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()

    # request = youtube.videos().insert(
    #     part="snippet,status",
    #     body={
    #       "snippet": {
    #         "categoryId": "22",
    #         "description": "Description of uploaded video.",
    #         "title": "Test video upload."
    #       },
    #       "status": {
    #         "privacyStatus": "private"
    #       }
    #     },
        
    #     # TODO: For this request to work, you must replace "YOUR_FILE"
    #     #       with a pointer to the actual file you are uploading.
    #     media_body=MediaFileUpload("/home/kefeh/Music/goodnews")
    # )

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics,player",
        id="U73sYiT1R8M"
    )

    response = request.execute()
    from pprint import pprint
    pprint(response)

if __name__ == "__main__":
    main()