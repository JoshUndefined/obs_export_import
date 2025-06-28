import json
import os
from obs_client import OBSClient

async def import_scene(config_path: str, asset_dir="assets"):
    with open(config_path, "r") as f:
        config = json.load(f)

    scene_name = config["scene_name"]
    client = OBSClient()
    await client.connect()

    await client.create_scene(scene_name)

    for src in config["sources"]:
        settings = src["settings"]

        # Update media file path if needed
        if src.get("local_file"):
            file_key = "local_file"  # adapt key for different source types
            if "local_file" in settings:
                settings["local_file"] = os.path.abspath(os.path.join(asset_dir, os.path.basename(src["local_file"])))

        await client.create_source(
            scene_name,
            src["name"],
            src["type"],
            settings,
            src.get("transform", {})
        )

        for filt in src.get("filters", []):
            await client.add_filter(src["name"], filt)

    await client.disconnect()
    print(f"Scene '{scene_name}' imported from {config_path}")
