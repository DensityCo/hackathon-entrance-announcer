from websocket import create_connection

import random
import json
import os
import requests
import subprocess

api_token = os.environ.get('WEBSOCKET_TOKEN', None)
if api_token is None:
    raise Exception("Please set the 'WEBSOCKET_TOKEN' environment variable")

api_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(api_token),
}

api_socket_response = requests.post(
    'https://api.density.io/v2/sockets/',
    headers=api_headers
).json()
websocket_url = api_socket_response['url']

sound_options = ["Basso", "Blow", "Bottle", "Frog", "Funk", "Glass", "Hero", "Morse", "Ping", "Pop", "Purr", "Sosumi", "Submarine", "Tink"]

ws = create_connection("{0}".format(websocket_url))
print "Receiving..."

while True:
    result =  json.loads(ws.recv())
    space = result['payload']['space_id']
    if space == 'spc_31879203125199140':
        if result['payload']['direction'] == 1:
            print "entered office"
            sound = random.choice(sound_options)
            print sound
            subprocess.call(["afplay", "/System/Library/Sounds/{0}.aiff".format(sound)])
        if result['payload']['direction'] == -1:
            print "exited office"
            sound = random.choice(sound_options)
            print sound
            subprocess.call(["afplay", "/System/Library/Sounds/{0}.aiff".format(sound)])
