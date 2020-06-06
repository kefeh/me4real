from bson import ObjectId
from datetime import datetime


def save_video(title, link, rank, _id=None):
    from models import db
    rank = int(rank)
    some_rank = int(rank)
    value = update_ranks(some_rank)

    video_item = db.Video() if not _id else db.Video.find_one({'_id': ObjectId(_id)})

    if value:
        video_item['title'] = title
        video_item['link'] = link
        video_item['date'] = str(datetime.now())
        video_item['rank'] = rank
        try:
            video_item.save()
        except Exception as exp:
            raise
            return {'failed_msg': "Database issues, unable to save Video, contact admin"}
    else:
        return {'failed_msg': "Database issues, unable to save Video, contact admin"}

    return get_video(cond=dict(video_item))


def update_ranks(rank):

    from models import db
    rank = int(rank)
    aldy_handled = ''
    while rank:
        some_video = db.Video.find_one({'_id': {'$ne': ObjectId(aldy_handled)}, 'rank': rank}) if aldy_handled else db.Video.find_one({'rank': rank})
        if not some_video:
            return True
        rank += 1
        some_video['rank'] = rank
        try:
            some_video.save()
            aldy_handled = some_video.get('_id')
        except Exception as exp:
            # raise
            return False

    return True


def update_rank_reverse(rank):

    from models import db
    rank = int(rank)
    while rank:
        fwd_rank = rank + 1
        some_video = db.Video.find_one({'rank': fwd_rank})
        if not some_video:
            return True
        some_video['rank'] = rank
        try:
            some_video.save()
            rank += 1
        except Exception as exp:
            return False
    
    return True


def get_video(maximum=None, cond={}):
    from models import db
    if maximum:
        video = list(db.Video.find({}).sort([('rank', 1)]).limit(int(maximum))) if not cond else list(db.Video.find(cond).sort([('rank', 1)]).limit(int(maximum)))
    else:
        video = list(db.Video.find({})) if not cond else list(db.Video.find(cond))
    for an_item in video:
        an_item['_id'] = str(an_item['_id'])
    return video if (maximum or not cond) else video[0]


def delete_video(video_id):
    from models import db
    try:
        a_video = db.Video.find_one({'_id': ObjectId(video_id)})
        db.Video.collection.remove({'_id': ObjectId(video_id)})
        update_rank_reverse(a_video['rank'])
    except Exception as exp:
        return {'fail_msg': 'Unable to delete the video item with that id'}, 404

    return {'pass_msg': 'successfully deleted'}, 204


# # -*- coding: utf-8 -*-

# # Sample Python code for youtube.channels.list
# # See instructions for running these code samples locally:
# # https://developers.google.com/explorer-help/guides/code_samples#python

# import os
# import base64
# import pickle

# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors

# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.http import MediaFileUpload


# from m_dir import BASE_PATH

# # the token.pickel file holds the credentials and you need to deploy it to server to be able to
# # access your email from the server
# TOKEN_PICKLE = f"{BASE_PATH}/token.pickle"
# CREDENTIALS = f"{BASE_PATH}/credentials.json"

# SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.upload"]


# api_service_name = "youtube"
# api_version = "v3"
# # client_secrets_file = "client_secret_864246643627-106pb92mqtq6t63jodls8tmhebqr824u.apps.googleusercontent.com.json"
# creds = None
# # The file token.pickle stores the user's access and refresh tokens, and is
# # created automatically when the authorization flow completes for the first
# # time.
# if os.path.exists(TOKEN_PICKLE):
#     with open(TOKEN_PICKLE, 'rb') as token:
#         creds = pickle.load(token)
# # If there are no (valid) credentials available, let the user log in.
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             CREDENTIALS, SCOPES)
#         creds = flow.run_local_server(port=8081)
#     # Save the credentials for the next run
#     with open(TOKEN_PICKLE, 'wb') as token:
#         pickle.dump(creds, token)

# youtube = googleapiclient.discovery.build(
#     api_service_name, api_version, credentials=creds)


# def upload_video(file_name, title, description):
#     try:
#         request = youtube.videos().insert(
#             part="snippet,status,player",
#             body={
#             "snippet": {
#                 "categoryId": "22",
#                 "description": description,
#                 "title": title
#             },
#             "status": {
#                 "privacyStatus": "public"
#             }
#             },
#             media_body=MediaFileUpload(file_name)
#         )
#         response = request.execute()

#         # the response has a player key which looks like 
#         #'player': {'embedHtml': '<iframe width="480" height="270" '
#                                 # 'src="//www.youtube.com/embed/U73sYiT1R8M" '
#                                 # 'frameborder="0" allow="accelerometer; '
#                                 # 'autoplay; encrypted-media; gyroscope; '
#                                 # 'picture-in-picture" '
#                                 # 'allowfullscreen></iframe>'},

#         embedHTML = response.get('player').get('embedHtml')
#         link = embedHTML.split("'src=", 1)[1].split("'", 1)[0].strip('"')
#     except Exception as exp:
#         print(exp)
#         return None
#     return link, title


# def video_decode_save(video, title, description):
#     """
#         This function takes in an image and an id/category which it will use as an image name and
#         then saves the image in the images folder and returns the appropriate path name for that
#         image
#     """

#     bucket = 'me4real-storage'

#     video_info = video.split(';')[0].split(':')[-1]
#     some_video = video.split(';')[1].split('base64,')[-1] + '=='
#     video_ext = video_info.split('/')[-1]
#     from m_dir import BASE_video_PATH
#     import os

#     f_video_name = video_name + '.' + video_ext
#     video_path = os.path.join(BASE_VIDEO_PATH, f_video_name)
#     # video_data = base64.b64decode(video)
#     if not os.path.exists(BASE_VIDEO_PATH):
#         os.makedirs(BASE_VIDEO_PATH)
#     with open(video_path, 'wb') as video_file:
#         video_file.write(base64.decodebytes(some_video.encode()))

#     response = upload_video(video_path, title, description)
#     print(response)
#     response = {'url': response[0], 'title': response[1]} if response else {'error': "Could not save the video contact admin"}

#     # Delete the temporal videos folder and all its contents
#     import shutil
#     try:
#         shutil.rmtree(BASE_VIDEO_PATH)
#     except OSError as e:
#         print ("Error: %s - %s." % (e.filename, e.strerror))

#     return response