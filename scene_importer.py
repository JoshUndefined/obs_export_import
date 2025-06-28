import json
import os
from obs_client import OBSClient

async def import_scene(config_path: str, asset_dir="assets"):
    with open(config_path, "r") as f:
        config = json.load(f)
    # print(config)

    scene_name = config["scene_name"]
    client = OBSClient()
    await client.connect()

    await client.create_scene(scene_name)

    for item in config["sources"]:
        print("================scene_item=============")
        # print(f"item: {item}")
        settings = item["settings"]
        # print(f"item: {settings}")

        # Update media file path if needed
        if item.get("local_file"):
            if "file" in settings:
                settings["file"] = os.path.abspath(os.path.join(asset_dir, os.path.basename(item["local_file"])))
                print("new file name: {}".format(settings["file"]))

        await client.create_source(
            scene_name,
            item["name"],
            item["type"],
            settings,
            item.get("transform", {})
        )

        for filt in item.get("filters", []):
            await client.add_filter(item["name"], filt)

    await client.disconnect()
    # print(f"Scene '{scene_name}' imported from {config_path}")
