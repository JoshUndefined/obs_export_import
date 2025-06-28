import os
from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)
import simpleobsws

#  Load config
load_dotenv()
OBS_WS_HOST = os.environ.get("OBS_WS_HOST")
OBS_WS_PORT = os.environ.get("OBS_WS_PORT")
OBS_WS_PASS = os.environ.get("OBS_WS_PASS")

class OBSClient:
    def __init__(self):
        url = f"ws://{OBS_WS_HOST}:{OBS_WS_PORT}"
        self.ws = simpleobsws.WebSocketClient(url=url, password=OBS_WS_PASS)

    async def connect(self):
        await self.ws.connect()
        await self.ws.wait_until_identified()

    async def disconnect(self):
        await self.ws.disconnect()

    async def get_version(self):
        result = await self.ws.call(simpleobsws.Request("GetVersion"))
        logger.info(f"get_version() = {result.responseData.get('obsVersion')}")
        return result.responseData.get("obsVersion")

    async def get_scene_items(self, scene_name):
        logger.info(f"get_scene_items({scene_name})")
        result = await self.ws.call(simpleobsws.Request("GetSceneItemList", {"sceneName": scene_name}))
        # logger.debug(result)
        return result.responseData.get("sceneItems", [])

    async def get_source_settings(self, source_name):
        logger.info(f"get_source_settings({source_name})")
        result = await self.ws.call(simpleobsws.Request("GetInputSettings", {"inputName": source_name}))
        return result.responseData

    async def get_source_filters(self, source_name):
        logger.info(f"get_source_filters({source_name})")
        result = await self.ws.call(simpleobsws.Request("GetSourceFilterList", {"sourceName": source_name}))
        return result.responseData.get("filters", [])

    async def create_scene(self, scene_name):
        logger.info(f"create_scene({scene_name})")
        await self.ws.call(simpleobsws.Request("CreateScene", {"sceneName": scene_name}))

    async def create_source(self, scene_name, source_name, source_kind, settings, transform):
        logger.info(f"create_source({source_name})")
        # logger.debug(f"scene_name: {scene_name}")
        # logger.debug(f"source_name: {source_name}")
        # logger.debug(f"source_kind: {source_kind}")
        # logger.debug(f"settings: {settings}")
        # logger.debug(f"transform: {transform}")
        logger.debug("parameters: {}".format({
            "sceneName": scene_name,
            "inputName": source_name,
            "inputKind": source_kind,
            "inputSettings": settings,
            # "sceneItemTransform": transform,
            "sceneItemEnabled": True
        }))
        result = await self.ws.call(simpleobsws.Request("CreateInput", {
            "sceneName": scene_name,
            "inputName": source_name,
            "inputKind": source_kind,
            "inputSettings": settings,
            "sceneItemTransform": transform,
            "sceneItemEnabled": True
        }))
        logger.debug(result)
        source_uuid = result.responseData["sceneItemId"]
        logger.debug(f"source_uuid: {source_uuid}")
        await self.set_transform(
            scene_name=scene_name,
            source_uuid=source_uuid,
            transform_data=transform
        )

    async def add_filter(self, source_name, filter_data):
        logger.info(f"add_filter({source_name})")
        await self.ws.call(simpleobsws.Request("CreateSourceFilter", {
            "sourceName": source_name,
            **filter_data
        }))

    async def set_transform(self, scene_name, source_uuid, transform_data):
        logger.info(f"set_transform(source_uuid: {source_uuid})")
        logger.debug(f"transform_data: {transform_data}")
        #  If bounding data is disabled, exporter sets to zero. Remove or SetSceneItemTransform fails
        if(transform_data["boundsType"] == "OBS_BOUNDS_NONE"):
            del transform_data["boundsWidth"]
            del transform_data["boundsHeight"]

        result = await self.ws.call(simpleobsws.Request("SetSceneItemTransform", {
            "sceneName": scene_name,
            "sceneItemId": source_uuid,
            "sceneItemTransform": transform_data
        }))
        logger.debug(result)
