from websocket import create_connection

import random
import json
import os
import requests
import subprocess

api_token = os.environ.get('WEBSOCKET_TOKEN', None)
if api_token is None:
    raise Exception("Please set the 'WEBSOCKET_TOKEN' environment variable")

sound_directory = os.environ.get('SOUND_DIRECTORY', None)
if api_token is None:
    raise Exception("Please set the 'SOUND_DIRECTORY' environment variable")

api_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(api_token),
}

sound_options = [ "steve_laugh"]

def new_websocket_url():
    api_socket_response = requests.post(
        'https://api.density.io/v2/sockets/',
        headers=api_headers
    ).json()
    return api_socket_response['url']

websocket_url = new_websocket_url()
ws = create_connection("{0}".format(websocket_url))
print "Receiving"

while True:
    try:
        result = json.loads(ws.recv())
        space = result['payload']['space_id']
        print result
        if space == 'spc_31879203125199140':
            if result['payload']['direction'] == 1:
                print "entered office"
                sound = random.choice(sound_options)
                print sound
                # subprocess.call(["afplay", "{0}/{1}.aif".format(sound_directory, sound)])   # mac
                subprocess.call(["play", "{0}/{1}.aif".format(sound_directory, sound)])   # Pi

    except Exception as e:
        print "{0}".format(e)
        # subprocess.call(["say", "websocket closed, reconnecting"])   # Pi
        # subprocess.call(["espeak", '"websocket closed, reconnecting" 2>/dev/null'])   # Pi
        # get new websocket_url
        websocket_url = new_websocket_url()
        ws = create_connection("{0}".format(websocket_url))
        print "reconnecting"
