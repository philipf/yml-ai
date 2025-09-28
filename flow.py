from pocketflow import AsyncFlow
from nodes import LoadConfigNode, FetchTopStoriesNode, AnalyzeStoriesNode, SortStoriesNode, GenerateSiteNode

def create_hn_digest_flow():
    """Creates and returns the HN Digest flow."""
    load_config_node = LoadConfigNode()
    fetch_stories_node = FetchTopStoriesNode()
    analyze_stories_node = AnalyzeStoriesNode()
    sort_stories_node = SortStoriesNode()
    generate_site_node = GenerateSiteNode()

    load_config_node >> fetch_stories_node >> analyze_stories_node >> sort_stories_node >> generate_site_node

    return AsyncFlow(start=load_config_node)
