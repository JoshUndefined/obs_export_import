# OBS Export/Import

import os
from dotenv import load_dotenv
import asyncio
import simpleobsws

#  Load config
load_dotenv()
OBS_WS_HOST = os.environ.get("OBS_WS_HOST")
OBS_WS_PORT = os.environ.get("OBS_WS_PORT")
OBS_WS_PASS = os.environ.get("OBS_WS_PASS")
url = f"ws://{OBS_WS_HOST}:{OBS_WS_PORT}"

# Configure OBS WS 5.x connection
parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False)
ws = simpleobsws.WebSocketClient(url = url, password = OBS_WS_PASS, identification_parameters  = parameters)


async def make_request():
    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

    request = simpleobsws.Request('GetVersion') # Build a Request object

    ret = await ws.call(request) # Perform the request
    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))

    await ws.disconnect() # Disconnect from the websocket server cleanly

loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())






# Given SceneName, gather the Scene Inputs and dependancies, generate a config file and export

# To import, run OBS WS API and dynamically re-generate the Scene Input