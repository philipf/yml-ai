import asyncio
import logging
from pocketflow import Node, AsyncParallelBatchNode
from utils.config import load_config
from utils.hackernews import get_top_story_ids, get_item_async, get_comments_async
from utils.web import crawl_async
from utils.static_site import generate
from utils.call_llm import call_llm_async

class LoadConfigNode(Node):
    def exec(self, _):
        logging.info("Loading configuration...")
        return load_config()

    def post(self, shared, _, exec_res):
        shared["config"] = exec_res
        shared["semaphore"] = asyncio.Semaphore(exec_res["api_concurrency"])
        logging.info("Configuration loaded.")

class FetchTopStoriesNode(Node):
    def prep(self, shared):
        return shared["config"]["top_stories_limit"]

    def exec(self, limit):
        logging.info(f"Fetching top {limit} stories...")
        return get_top_story_ids(limit)

    def post(self, shared, _, exec_res):
        shared["top_story_ids"] = exec_res
        logging.info(f"{len(exec_res)} top stories fetched.")

class AnalyzeStoriesNode(AsyncParallelBatchNode):
    async def prep_async(self, shared):
        logging.info("Preparing to analyze stories...")
        return [(story_id, shared['config'], shared['semaphore']) for story_id in shared["top_story_ids"]]

    async def exec_async(self, item):
        story_id, config, semaphore = item
        logging.info(f"Analyzing story {story_id}...")
        story = await get_item_async(story_id, semaphore=semaphore)
        if not story or story.get('deleted') or story.get('dead') or not story.get('url'):
            logging.warning(f"Skipping story {story_id} as it is deleted, dead, or has no URL.")
            return None

        try:
            # Run fetching comments and article content concurrently
            comments_task = get_comments_async(story, config["comments_limit"], semaphore=semaphore)
            article_content_task = crawl_async(story.get('url'), semaphore=semaphore)
            comments, article_content = await asyncio.gather(comments_task, article_content_task)
        except Exception as e:
            logging.warning(f"Skipping story {story_id} due to error fetching content: {e}")
            return None

        context = f"""Title: {story.get('title')}
Article Content: {article_content[:2000]}

Comments:
"""
        for comment in comments:
            context += f"- {comment.get('text', '')}\n"

        prompt = f"""Analyze the following Hacker News story and determine if it is relevant to any of these topics: {config['areas_of_interest']}.

{context}

Provide a summary, no longer than two sentences, base it of the title, article content and comments. If it is not relevant to any the topics, respond with 'NO'.
The summary must be highly concise and must not begin with an introductory phrase such as 'The post describes,' 'This thread explains,' or 'The article discusses.' Start the summary directly with the main subject.

Your response should be either 'NO' or a short summary."""

        summary = await call_llm_async(prompt, semaphore=semaphore)

        if "NO" in summary.upper():
            logging.info(f"Story {story_id} is not relevant.")
            return None

        logging.info(f"Story {story_id} is relevant.")
        story['summary'] = summary
        return story

    async def post_async(self, shared, _, exec_res_list):
        shared["interesting_stories"] = [story for story in exec_res_list if story]
        logging.info(f"{len(shared['interesting_stories'])} interesting stories found.")

class SortStoriesNode(Node):
    def prep(self, shared):
        return shared["interesting_stories"]

    def exec(self, stories):
        logging.info("Sorting stories by points...")
        return sorted(stories, key=lambda x: x.get('score', 0), reverse=True)

    def post(self, shared, _, exec_res):
        shared["interesting_stories"] = exec_res
        logging.info("Stories sorted.")

class GenerateSiteNode(Node):
    def prep(self, shared):
        return shared["interesting_stories"]

    def exec(self, stories):
        logging.info("Generating static site...")
        return generate(stories)

    def post(self, shared, _, exec_res):
        shared["html_output"] = exec_res
        with open("index.html", "w") as f:
            f.write(exec_res)
        logging.info("Static site generated.")
