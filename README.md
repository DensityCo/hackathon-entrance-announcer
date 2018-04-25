## Setup environment:

In terminal run following commands:
$ pip --version
If response is `-bash: command not found` do following:
  $ easy_install pip

Then:
$ pip install websocket-client==0.47.0
$ pip install requests==2.13.0

## Environment variables:
go to following url and copy "hackathon announcer token" token:
https://dashboard.density.io/#/dev/tokens

Websocket token
$ export WEBSOCKET_TOKEN=<hackathon_token>

Space_id:
go to following url and copy space_id of the dpu that you want to connect to
https://dashboard.density.io/#/spaces/insights/
Click on the space you will connect to.
Then copy `spc_` code from the end of the browser url. ex `spc_0987097097987`

In terminal:
$ export SPACE_ID=<spc_code>
