import json
import os
import logging
logger = logging.getLogger(__name__)
from .obs_client import OBSClient

async def import_scene(scene_name: str):
    config_path = f"output/{scene_name}/{scene_name}.json"
    asset_dir = f"output/{scene_name}/assets"
    with open(config_path, "r") as f:
        config = json.load(f)
    # logger.debug(config)

    scene_name = config["scene_name"]
    client = OBSClient()
    await client.connect()

    await client.create_scene(scene_name)

    for item in config["sources"]:
        logger.info("==== scene_item ====")
        # logger.debug(f"item: {item}")
        settings = item["settings"]
        # logger.debug(f"item: {settings}")

        # Update media file path if needed
        if item.get("local_file"):
            if "file" in settings:
                settings["file"] = os.path.abspath(os.path.join(asset_dir, os.path.basename(item["local_file"])))
                logger.info("new file name: {}".format(settings["file"]))

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
    logger.info(f"Scene '{scene_name}' imported from {config_path}")
