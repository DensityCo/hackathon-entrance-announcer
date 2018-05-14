from websocket import create_connection
import requests

import random
import json
import os
import subprocess
import sys
sys.path.insert(0, '/home/pi/iBeacon-Scanner-/')
import blescan

import bluetooth._bluetooth as bluez

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

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

    # while True:
    # try:
            # result = json.loads(ws.recv())
            # space = result['payload']['space_id']
            # print result
            # TEMP until dpu set up if space == space_id:
            #     if result['payload']['direction'] == 1:
    print "entered office"
    returnedList = blescan.parse_events(sock, 10) 
    charissa = False
    for beacon in returnedList:
        if '7b44b47b52a1538190c2f09b6838c5d4' in beacon:
            charissa = True
    if charissa:
        print "hi charissa"
    print sound_directory
    sound = random.choice(sound_options)
    print sound
    print "{0}/{1}.aif".format(sound_directory, sound)

    subprocess.call(["afplay", "{0}/{1}.aif".format(sound_directory, sound)])   # mac

    # except Exception as e:
    #    print "{0}".format(e)
    #    websocket_url = new_websocket_url(websocket_token)
    #    ws = create_connection("{0}".format(websocket_url))
    #    print "reconnecting"
