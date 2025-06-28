import asyncio
import argparse
from lib.scene_importer import import_scene

parser = argparse.ArgumentParser(
    description="Imports a saved OBS scene from JSON and rebuilds it in OBS"
)
parser.add_argument("scene", help="Scene name to import", type=str)
args = parser.parse_args()

async def main():
    await import_scene(f"output/packaged_scenes/{args.scene}.json")

if __name__ == "__main__":
    asyncio.run(main())
