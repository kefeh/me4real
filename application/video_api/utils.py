# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# the token.pickel file holds the credentials and you need to deploy it to server to be able to
# access your email from the server
TOKEN_PICKLE = f"{BASE_DIR}/token.pickle"
CREDENTIALS = f"{BASE_DIR}/credentials.json"

SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.upload"]


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


def save_video(file_name, title, description):
    request = youtube.videos().insert(
        part="snippet,status,player",
        body={
          "snippet": {
            "categoryId": "22",
            "description": description,
            "title": title
          },
          "status": {
            "privacyStatus": "public"
          }
        },
        media_body=MediaFileUpload(file_name)
    )
    response = request.execute()

    # the response has a player key which looks like 
    #'player': {'embedHtml': '<iframe width="480" height="270" '
                            # 'src="//www.youtube.com/embed/U73sYiT1R8M" '
                            # 'frameborder="0" allow="accelerometer; '
                            # 'autoplay; encrypted-media; gyroscope; '
                            # 'picture-in-picture" '
                            # 'allowfullscreen></iframe>'},

    embedHTML = response.get('player').get('embedHtml')
    link = embedHTML.split("'src=", 1)[1].split("'", 1)[0].strip('"')
    return link


def get_embedded_link(ID):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics,player",
        id=ID
    )

    response = request.execute()
    from pprint import pprint
    pprint(response)


