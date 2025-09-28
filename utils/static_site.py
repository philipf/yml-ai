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
        body {{ font-family: Arial, Verdana, Tahoma, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; padding: 20px; border-radius: 8px; }}
        h1 {{ text-align: center; }}
        p.date {{ text-align: center; }}
        .story {{ margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid; }}
        .story:last-child {{ border-bottom: none; }}
        .story h2 {{ margin: 0 0 10px 0; }}
        .story h2 a {{ text-decoration: none; }}
        .story h2 a:hover {{ text-decoration: underline; }}
        .story .meta {{ font-size: 0.9em; }}
        .story .meta a {{ color: inherit; text-decoration: none; }}
        .story .meta a:hover {{ text-decoration: underline; }}
        .story .summary {{ margin-top: 10px; }}
        
        .theme-switch-wrapper {{ position: fixed; top: 20px; right: 20px; display: flex; align-items: center; }}
        .theme-switch {{ display: inline-block; height: 34px; position: relative; width: 60px; }}
        .theme-switch input {{ display:none; }}
        .slider {{ background-color: #ccc; bottom: 0; cursor: pointer; left: 0; position: absolute; right: 0; top: 0; transition: .4s; }}
        .slider:before {{ background-color: #fff; bottom: 4px; content: ""; height: 26px; left: 4px; position: absolute; transition: .4s; width: 26px; }}
        input:checked + .slider {{ background-color: #2196F3; }}
        input:checked + .slider:before {{ transform: translateX(26px); }}
        .slider.round {{ border-radius: 34px; }}
        .slider.round:before {{ border-radius: 50%; }}

        /* Dark Mode (default) */
        body.dark-mode {{ background-color: #121212; color: #e0e0e0; }}
        .dark-mode .container {{ background: #1e1e1e; box-shadow: 0 0 10px rgba(255,255,255,0.1); }}
        .dark-mode h1 {{ color: #ff6600; }}
        .dark-mode p.date {{ color: #828282; }}
        .dark-mode .story {{ border-bottom-color: #333; }}
        .dark-mode .story h2 a {{ color: #80C0FF; }}
        .dark-mode .meta {{ color: #828282; }}

        /* Light Mode */
        body.light-mode {{ background-color: #f9f9f9; color: #333; }}
        .light-mode .container {{ background: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .light-mode h1 {{ color: #ff6600; }}
        .light-mode p.date {{ color: #828282; }}
        .light-mode .story {{ border-bottom-color: #eee; }}
        .light-mode .story h2 a {{ color: #000; }}
        .light-mode .meta {{ color: #828282; }}
    </style>
</head>
<body>
    <div class="theme-switch-wrapper">
        <label class="theme-switch" for="checkbox">
            <input type="checkbox" id="checkbox" />
            <div class="slider round"></div>
        </label>
        <span style="margin-left: 10px;">🌙</span>
    </div>
    <div class="container">
        <h1>HN Digest</h1>
        <p class="date">{date}</p>
"""

    for story in stories:
        html += f"""        <div class="story">
            <h2><a href="{story['url']}" target="_blank">{story['title']}</a></h2>
            <div class="meta">{story['score']} points | <a href="https://news.ycombinator.com/item?id={story['id']}" target="_blank">{story.get('descendants', 0)} comments</a></div>
            <div class="summary">{story['summary']}</div>
        </div>
"""

    html += """    </div>
    <script>
        const checkbox = document.getElementById('checkbox');
        checkbox.addEventListener('change', () => {
            const body = document.body;
            if (body.classList.contains('dark-mode')) {
                body.classList.remove('dark-mode');
                body.classList.add('light-mode');
                localStorage.setItem('theme', 'light-mode');
            } else {
                body.classList.remove('light-mode');
                body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark-mode');
            }
        });

        // Apply the saved theme on load
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.body.classList.add(savedTheme);
            if (savedTheme === 'light-mode') {
                checkbox.checked = true;
            }
        } else {
            document.body.classList.add('dark-mode');
        }
    </script>
</body>
</html>"""

    return html
