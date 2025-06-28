import asyncio
import argparse
from scene_exporter import export_scene

parser = argparse.ArgumentParser("test_export")
parser.add_argument("scene", help="Scene name to export", type=str)
args = parser.parse_args()

async def main():
    await export_scene(args.scene)

if __name__ == "__main__":
    asyncio.run(main())
