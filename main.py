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


async def make_request(requestName, requestData):
    print("===================================")
    print(f"make_request({requestName}):")
    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete
    # request = simpleobsws.Request('GetVersion') # Build a Request object
    request = simpleobsws.Request(requestName, requestData)
    # print(request)
    ret = await ws.call(request) # Perform the request

    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))
        return ret.responseData
    else:
        print("Request failed! Response: {}".format(ret.requestStatus))
    await ws.disconnect() # Disconnect from the websocket server cleanly


loop = asyncio.get_event_loop()

# Make a rectangle
res = loop.run_until_complete(
    make_request('CreateInput', {
        "sceneName":"Scene",
        "inputName":"rectangle1",
        "inputKind":"color_source_v3",
        "inputSettings":{
            "color":4291940817,
            "width":109,
            "height":200
        },
        "sceneItemEnabled":True
    }
))
print("===================================")

# Get rectangle sceneItemId
# print(res)
sceneItemId = res["sceneItemId"]
# sceneItemId = 20
# print(sceneItemId)

# Move the rectangle
loop.run_until_complete(
    make_request(
        'SetSceneItemTransform',
        {
            "sceneName": "Scene",
            "sceneItemId": sceneItemId,
            "sceneItemTransform": {
                "alignment": 5,
                "boundsAlignment": 0,
                # "boundsHeight": 0,
                "boundsType": "OBS_BOUNDS_NONE",
                # "boundsWidth": 0,
                "cropBottom": 0,
                "cropLeft": 0,
                "cropRight": 0,
                "cropToBounds": False,
                "cropTop": 0,
                "height": 400,
                "positionX": 150,
                "positionY": 300,
                "rotation": 0,
                "scaleX": 1,
                "scaleY": 1,
                "sourceHeight": 200,
                "sourceWidth": 109,
                "width": 209
            }
        }
    ))





# Given SceneName, gather the Scene Inputs and dependancies, generate a config file and export

# To import, run OBS WS API and dynamically re-generate the Scene Input