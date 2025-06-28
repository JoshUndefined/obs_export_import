import os
import json
import logging
logger = logging.getLogger(__name__)
from .obs_client import OBSClient
from .utils import sanitize_filename, download_media_file

async def export_scene(scene_name: str, output_dir="output/packaged_scenes", asset_dir="output/assets"):
    client = OBSClient()
    await client.connect()

    # ver = await client.get_version()
    # logger.debug(ver)

    # Get scene sources
    scene_items = await client.get_scene_items(scene_name)
    # logger.debug(scene_items)

    packaged_data = {
        "scene_name": scene_name,
        "sources": []
    }

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(asset_dir, exist_ok=True)

    for item in scene_items:
        logger.info("==== scene_item ====")

        source = await client.get_source_settings(item["sourceName"])
        logger.debug(f"source: {source}")
        filters = await client.get_source_filters(item["sourceName"])
        # logger.debug(f"filters: {filters}")
        transform = item["sceneItemTransform"]
        # logger.debug(f"transform: {transform}")

        # Check and download media if needed
        local_path = None
        if source["inputKind"] in ["ffmpeg_source", "image_source", "input"]:
            local_path = download_media_file(source["inputSettings"], asset_dir)
            # logger.debug(source["inputKind"])

        packaged_data["sources"].append({
            "name": item["sourceName"],
            "type": source["inputKind"],
            "settings": source["inputSettings"],
            "filters": filters,
            "transform": transform,
            "local_file": local_path
        })
    
    logger.debug(scene_items)

    filename = os.path.join(output_dir, f"{sanitize_filename(scene_name)}.json")
    with open(filename, "w") as f:
        json.dump(packaged_data, f, indent=2)

    await client.disconnect()
    logger.info(f"Scene '{scene_name}' exported to {filename}")
