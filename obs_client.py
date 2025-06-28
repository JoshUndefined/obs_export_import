import simpleobsws

class OBSClient:
    def __init__(self):
        self.ws = simpleobsws.WebSocketClient()

    async def connect(self):
        await self.ws.connect()
        await self.ws.wait_until_identified()

    async def disconnect(self):
        await self.ws.disconnect()

    async def get_scene_items(self, scene_name):
        result = await self.ws.call("GetSceneItemList", {"sceneName": scene_name})
        return result.get("sceneItems", [])

    async def get_source_settings(self, source_name):
        return await self.ws.call("GetInputSettings", {"inputName": source_name})

    async def get_source_filters(self, source_name):
        result = await self.ws.call("GetSourceFilterList", {"sourceName": source_name})
        return result.get("filters", [])

    async def create_scene(self, scene_name):
        await self.ws.call("CreateScene", {"sceneName": scene_name})

    async def create_source(self, scene_name, source_name, source_kind, settings, transform):
        await self.ws.call("CreateInput", {
            "sceneName": scene_name,
            "inputName": source_name,
            "inputKind": source_kind,
            "inputSettings": settings,
            "sceneItemTransform": transform
        })

    async def add_filter(self, source_name, filter_data):
        await self.ws.call("CreateSourceFilter", {
            "sourceName": source_name,
            **filter_data
        })
