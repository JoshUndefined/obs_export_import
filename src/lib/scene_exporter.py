import os
import json
import shutil
from .obs_client import OBSClient
from .utils import sanitize_filename, download_media_file

async def export_scene(scene_name: str, output_dir="output/packaged_scenes", asset_dir="output/assets"):
    client = OBSClient()
    await client.connect()

    # ver = await client.get_version()
    # print(ver)

    # Get scene sources
    scene_items = await client.get_scene_items(scene_name)
    # print(scene_items)

    packaged_data = {
        "scene_name": scene_name,
        "sources": []
    }

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(asset_dir, exist_ok=True)

    for item in scene_items:
        print("================scene_item=============")

        source = await client.get_source_settings(item["sourceName"])
        print(f"source: {source}")
        filters = await client.get_source_filters(item["sourceName"])
        # print(f"filters: {filters}")
        transform = item["sceneItemTransform"]
        # print(f"transform: {transform}")

        # Check and download media if needed
        local_path = None
        if source["inputKind"] in ["ffmpeg_source", "image_source", "input"]:
            local_path = download_media_file(source["inputSettings"], asset_dir)
            # print(source["inputKind"])

        packaged_data["sources"].append({
            "name": item["sourceName"],
            "type": source["inputKind"],
            "settings": source["inputSettings"],
            "filters": filters,
            "transform": transform,
            "local_file": local_path
        })
    
    print(scene_items)

    filename = os.path.join(output_dir, f"{sanitize_filename(scene_name)}.json")
    with open(filename, "w") as f:
        json.dump(packaged_data, f, indent=2)

    await client.disconnect()
    print(f"Scene '{scene_name}' exported to {filename}")
