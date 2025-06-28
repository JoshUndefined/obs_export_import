import asyncio
import argparse
from lib.scene_exporter import export_scene

parser = argparse.ArgumentParser(
    description="Exports an OBS scene to JSON to rebuild in a separate OBS instance/scene collection"
)
parser.add_argument("scene", help="Scene name to export", type=str)
args = parser.parse_args()

async def main():
    await export_scene(args.scene)

if __name__ == "__main__":
    asyncio.run(main())
