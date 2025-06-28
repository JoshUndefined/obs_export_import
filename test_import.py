import asyncio
import argparse
from scene_importer import import_scene

parser = argparse.ArgumentParser("test_import")
parser.add_argument("scene", help="Scene name to import", type=str)
args = parser.parse_args()

async def main():
    # print(f"packaged_scenes/{args.scene}.json")
    await import_scene(f"packaged_scenes/{args.scene}.json")

if __name__ == "__main__":
    asyncio.run(main())
