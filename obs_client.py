import simpleobsws

class OBSClient:
    def __init__(self):
        self.ws = simpleobsws.WebSocketClient(url = "ws://localhost:4455")

    async def connect(self):
        await self.ws.connect()
        await self.ws.wait_until_identified()

    async def disconnect(self):
        await self.ws.disconnect()

    async def get_version(self):
        result = await self.ws.call(simpleobsws.Request("GetVersion"))
        print(f"get_version() = {result.responseData.get('obsVersion')}")
        return result.responseData.get("obsVersion")

    async def get_scene_items(self, scene_name):
        # print(f"get_scene_items({scene_name})")
        result = await self.ws.call(simpleobsws.Request("GetSceneItemList", {"sceneName": scene_name}))
        # print(result)
        return result.responseData.get("sceneItems", [])

    async def get_source_settings(self, source_name):
        # print(f"get_source_settings({source_name})")
        result = await self.ws.call(simpleobsws.Request("GetInputSettings", {"inputName": source_name}))
        return result.responseData

    async def get_source_filters(self, source_name):
        # print(f"get_source_filters({source_name})")
        result = await self.ws.call(simpleobsws.Request("GetSourceFilterList", {"sourceName": source_name}))
        return result.responseData.get("filters", [])

    async def create_scene(self, scene_name):
        print(f"create_scene({scene_name})")
        await self.ws.call(simpleobsws.Request("CreateScene", {"sceneName": scene_name}))

    async def create_source(self, scene_name, source_name, source_kind, settings, transform):
        print(f"create_source({source_name})")
        await self.ws.call(simpleobsws.Request("CreateInput", {
            "sceneName": scene_name,
            "inputName": source_name,
            "inputKind": source_kind,
            "inputSettings": settings,
            "sceneItemTransform": transform
        }))

    async def add_filter(self, source_name, filter_data):
        print(f"add_filter({source_name})")
        await self.ws.call(simpleobsws.Request("CreateSourceFilter", {
            "sourceName": source_name,
            **filter_data
        }))
