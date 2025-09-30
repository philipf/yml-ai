#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the main script
python main.py

# Add index.html to git stage
git add index.html

# Commit the changes with the specified message format and timezone
git commit -m "Latest run $(TZ='Pacific/Auckland' date +'%Y-%m-%d %H:%M')"

# Push the changes
git push
