import asyncio
import argparse
import logging
logger = logging.getLogger(__name__)
from lib.scene_importer import import_scene

async def main():
    parser = argparse.ArgumentParser(
        description="Imports a saved OBS scene from JSON and rebuilds it in OBS"
    )
    parser.add_argument("scene", help="Scene name to import", type=str)
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose debug output")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)8s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    for ext_logger in ['simpleobsws']:
        logging.getLogger(ext_logger).setLevel(logging.WARNING)

    logger.debug("Verbose logging enabled")
    logger.info(f"Importing scene: {args.scene}")

    await import_scene(args.scene)

if __name__ == "__main__":
    asyncio.run(main())
