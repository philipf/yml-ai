from datetime import datetime

def generate(stories: list):
    """Generates a static HTML site from a list of stories."""
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HN Digest</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f9f9f9; color: #333; }}
        .container {{ max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ text-align: center; color: #ff6600; }}
        p.date {{ text-align: center; color: #828282; }}
        .story {{ margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #eee; }}
        .story:last-child {{ border-bottom: none; }}
        .story h2 {{ margin: 0 0 10px 0; }}
        .story h2 a {{ color: #000; text-decoration: none; }}
        .story h2 a:hover {{ text-decoration: underline; }}
        .story .meta {{ font-size: 0.9em; color: #828282; }}
        .story .summary {{ margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>HN Digest</h1>
        <p class="date">{date}</p>
"""

    for story in stories:
        html += f"""        <div class="story">
            <h2><a href="{story['url']}" target="_blank">{story['title']}</a></h2>
            <div class="meta">{story['score']} points | {story.get('descendants', 0)} comments</div>
            <div class="summary"><strong>Summary:</strong> {story['summary']}</div>
        </div>
"""

    html += """    </div>
</body>
</html>"""

    return html
