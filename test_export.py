import asyncio
from scene_exporter import export_scene

async def main():
    await export_scene("KoalatyDono")

if __name__ == "__main__":
    asyncio.run(main())
