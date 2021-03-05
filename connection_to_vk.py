import vk
import os


confirmation_token = 'e9d2702e'
token = os.environ.get('vk_api_token')
session = vk.Session(access_token=token)
api = vk.API(session, v='5.130')
