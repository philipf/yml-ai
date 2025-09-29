# Hacker News Digest Generator


This project is a Hacker News digest generator that uses AI to analyze and summarize the top stories based on your interests. It's built using [Pocket Flow](https://github.com/The-Pocket/PocketFlow), a 100-line LLM framework.

## API Key Management

The application retrieves the Gemini API key in two ways:

1.  **Password Store (`pass`)**: It first attempts to retrieve the key from the `pass` password manager from the entry `gemini/apikey`. This is the recommended approach for security reasons.
2.  **Environment Variable**: If `pass` is not available or the key is not found, it falls back to reading the `GEMINI_API_KEY` environment variable.

You can modify `utils/call_llm.py` to change this behavior.

## How to Run

To generate the Hacker News digest, run:

```bash
python main.py
```

The output will be saved in `index.html`.

## Configuration

The `config.yml` file allows you to configure the digest generation:

-   `top_stories_limit`: The number of top stories to fetch from Hacker News.
-   `comments_limit`: The number of comments to fetch for each story.
-   `areas_of_interest`: A list of topics you are interested in. The AI will use these to filter and rank the stories.