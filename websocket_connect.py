from websocket import create_connection
import requests

import random
import json
import os
import subprocess

api_token = os.environ.get('WEBSOCKET_TOKEN', None)
if api_token is None:
    raise Exception("Please set the 'WEBSOCKET_TOKEN' environment variable")

space_id = os.environ.get('SPACE_ID', None)
if space_id is None:
    raise Exception("Please set the 'SPACE_ID' environment variable")

current_directory = os.path.dirname(os.path.realpath(__file__))
sound_directory = os.path.join(current_directory, 'sounds')

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
        if space == space_id:
            if result['payload']['direction'] == 1:
                print "entered office"
                sound = random.choice(sound_options)
                subprocess.call(["afplay", "{0}/{1}.aif".format(sound_directory, sound)])   # mac

    except Exception as e:
        print "{0}".format(e)
        websocket_url = new_websocket_url()
        ws = create_connection("{0}".format(websocket_url))
        print "reconnecting"
