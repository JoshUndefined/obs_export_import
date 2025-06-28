import os
import json
import shutil
from obs_client import OBSClient
from utils import sanitize_filename, download_media_file

async def export_scene(scene_name: str, output_dir="packaged_scenes", asset_dir="assets"):
    client = OBSClient()
    await client.connect()

    # Get scene sources
    scene_items = await client.get_scene_items(scene_name)

    packaged_data = {
        "scene_name": scene_name,
        "sources": []
    }

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(asset_dir, exist_ok=True)

    for item in scene_items:
        source = await client.get_source_settings(item["sourceName"])
        filters = await client.get_source_filters(item["sourceName"])
        transform = item.get("transform", {})

        # Check and download media if needed
        local_path = None
        if source["sourceKind"] in ["ffmpeg_source", "image_source", "input"]:
            local_path = download_media_file(source["settings"], asset_dir)

        packaged_data["sources"].append({
            "name": item["sourceName"],
            "type": source["sourceKind"],
            "settings": source["settings"],
            "filters": filters,
            "transform": transform,
            "local_file": local_path
        })

    filename = os.path.join(output_dir, f"{sanitize_filename(scene_name)}.json")
    with open(filename, "w") as f:
        json.dump(packaged_data, f, indent=2)

    await client.disconnect()
    print(f"Scene '{scene_name}' exported to {filename}")
