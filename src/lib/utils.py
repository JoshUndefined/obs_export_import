import os
import shutil
import logging
logger = logging.getLogger(__name__)

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)

def download_media_file(settings, asset_dir):
    # Generic handler: pull path and copy it to asset_dir
    file_keys = ["local_file", "file", "file_path"]
    for key in file_keys:
        if key in settings:
            src_path = settings[key]
            if os.path.isfile(src_path):
                dst_path = os.path.join(asset_dir, os.path.basename(src_path))
                shutil.copy2(src_path, dst_path)
                return dst_path
    return None
