import asyncio
import logging
from flow import create_hn_digest_flow

async def main():
    """The main entry point for the HN Digest application."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    shared = {
        "config": {},
        "top_story_ids": [],
        "interesting_stories": [],
        "html_output": ""
    }

    hn_digest_flow = create_hn_digest_flow()
    await hn_digest_flow.run_async(shared)

    logging.info("HN Digest generated successfully!")
    logging.info("You can find the output in the 'output/index.html' file.")

if __name__ == "__main__":
    asyncio.run(main())