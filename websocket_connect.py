from websocket import create_connection
import requests

import random
import json
import os
import subprocess


def new_websocket_url(websocket_token):
    api_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(websocket_token),
    }
    api_socket_response = requests.post(
        'https://api.density.io/v2/sockets/',
        headers=api_headers
    ).json()
    return api_socket_response['url']


def poll_websocket_for_events(sound_directory, space_id, websocket_token):
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
        websocket_url = new_websocket_url(websocket_token)
        ws = create_connection("{0}".format(websocket_url))
        print "reconnecting"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run announcer on a dpu")
    parser.add_argument('-w', '--webtoken', nargs='+', required=True,
                        help="Websocket Token. See Readme for instruction")
    parser.add_argument('-s', '--spaceid', nargs='+',
                        help="Space ID for DPU. See REadme for instruction")

    args = parser.parse_args()
    space_id = args.spaceid[0]
    websocket_token = args.webtoken[0]


    current_directory = os.path.dirname(os.path.realpath(__file__))
    sound_directory = os.path.join(current_directory, 'sounds')

    sound_options = [ "steve_laugh"]

    websocket_url = new_websocket_url(websocket_token)
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
            websocket_url = new_websocket_url(websocket_token)
            ws = create_connection("{0}".format(websocket_url))
            print "reconnecting"
