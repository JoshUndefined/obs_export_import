import asyncio
import argparse
from lib.scene_importer import import_scene

parser = argparse.ArgumentParser("import_scene")
parser.add_argument("scene", help="Scene name to import", type=str)
args = parser.parse_args()

async def main():
    # print(f"output/packaged_scenes/{args.scene}.json")
    await import_scene(f"output/packaged_scenes/{args.scene}.json")

if __name__ == "__main__":
    asyncio.run(main())
