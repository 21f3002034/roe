# GIT STARTING

```bash
git config --global user.name "21f3002034"

git config --global user.email "21f3002034@ds.study.iitm.ac.in"

git clone https://github.com/21f3002034/roe.git

git checkout -b main

git remote add origin https://github.com/21f3002034/roe.git
```

# when GIT on Error

```bash
git clone https://github.com/21f3002034/roe.git

git pull origin main --allow-unrelated-histories
```

# clear git history

```powershell
cmdkey /delete:git:https://github.com
#for linux echo url=https://github.com | git credential reject

git push -u origin main
git branch
git branch -m master main
git checkout -b main
git add .
git commit -m "Initial commit"

git push -u origin main
git config --global user.name
git config --global user.email
git config --global user.name "YourGitHubUsername"
git config --global user.email "your-email@example.com"
cmdkey /delete:git:https://github.com
git push -u origin main


#Go to GitHub → Settings → Developer settings → Personal access tokens
#👉 GitHub PAT Generator
#Click Generate new token (Choose "classic" if available).
#Select repo permissions.
#Copy the generated token.
#Now, use this token when Git asks for a password.


git pull --rebase origin main
git add .
git rebase --continue
git push -u origin main

git push -u origin main
git push --force origin main

git pull --rebase origin main
git push -u origin main
```

# PODMAN

```powershell
# building new docker image
podman build -t tds_project_final .
podman images
# running the image with image id b0aaad927709
podman run -p 5000:8000 1452c59bcedb 
podman run -p  5000:8000 -e AIPROXY_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIwMzRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.KEQjxQbjAIHY8_0l-WpiOL_KrBslnPTFZnexib9N6qc" f8564636db7c

podman rmi 1452c59bcedb

# looking for running containers with container id
podman ps
podman ps -a  
# starting or stopping or logs of container with container id
podman stop <container id>
podman start <container id>
podman logs <container id>

podman stop b679ecf5055a
podman rm b679ecf5055a

podman stop 661f5bf70fe0
podman rm 661f5bf70fe0
# container is like virtual machine that is isolated from local windows or other os

# pushing the image to docker hub website
docker push b0aaad927709 raghuvasanth/ds_project1_docker:tagname
podman pull raghuvasanth/ds_project1_docker:tagname
```

# running app with token

```powershell
uv run app.py AIPROXY_TOKEN='eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIwMzRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.KEQjxQbjAIHY8_0l-WpiOL_KrBslnPTFZnexib9N6qc'
uv run app.py AIPROXY_TOKEN=$AIPROXY_TOKEN
uv run EVAL.py --email 21f3002034@ds.study.iitm.ac.in
```

export AIPROXY_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIwMzRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.KEQjxQbjAIHY8_0l-WpiOL_KrBslnPTFZnexib9N6qc"
uvicorn app:app --host localhost --port 8000 --reload AIPROXY_TOKEN=$AIPROXY_TOKEN

> https://github.com/21f3002034/tds_project1
> raghuvasanth/tds_project1_docker:v1

# Docker Hub

```powershell
podman login docker.io
podman tag <IMAGE_ID> docker.io/<YOUR_DOCKER_USERNAME>/<IMAGE_NAME>:<TAG>
podman push docker.io/<YOUR_DOCKER_USERNAME>/<IMAGE_NAME>:<TAG>
podman tag e43f066c0ba0 docker.io/raghuvasanth/tds_project1_docker:final
podman push docker.io/raghuvasanth/tds_project1_docker:final
```

# ngrok

open ngrok.exe then enter below 

```powershell
ngrok config add-authtoken 2sMCnqP6qX4UdkP68YRTaK1Jd1m_Gk5FsHaFTj8fKC5iEMao

#before start the local server
ngrok http http://localhost:8000
```

# fast api setup

[Reference link](https://github.com/21f3002034/tds_project1/tree/main)[GitHub - 21f3002034/tds_project1](https://github.com/21f3002034/tds_project1/tree/main)

```python

https://github.com/21f3002034/tds_project1/tree/main# /// script
# requires-python = ">=3.13"
# dependencies = [
#       "flask",
#      "fastapi",
#      "uvicorn", 
#      "requests",
#      "pathlib",
#       "datetime",
#       "openai",
#       "pytesseract",
#       "numpy",
#       "pillow",
#       "sentence_transformers",
#       "scipy",
#      "pandas",
#       "markdown",
#   "SpeechRecognition",
#   "gitpython",
#   "python-multipart",
#   "duckdb",
#   "python-dateutil"
#   
# ]
# ///
import duckdb
import git
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import os
import subprocess
import json
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
import pytesseract
from PIL import Image
import shutil
import duckdb
import markdown
import json
import speech_recognition as sr


app = FastAPI()

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)



def query_gpt(user_input: str) -> Dict[str, Any]:
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"                    
    AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIwMzRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.KEQjxQbjAIHY8_0l-WpiOL_KrBslnPTFZnexib9N6qc""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": user_input},
            {
                "role": "system",
                "content": """
                
        You are an assistant capable of executing various tasks.  
        Use the following functions for specific tasks:  
        
        - Use 'script_runner' for running scripts.  
        - Use 'format_file' for formatting files.  
        - Use 'scrape_website_data' for scraping website data.  
        - Use 'process_csv' for handling CSV file operations.  
        - Use 'generate_report' for creating reports.  
        - Use 'parse_json' for parsing JSON data.  
        - Use 'extract_text' for extracting text from documents.  
        - Use 'translate_text' for translating text between languages.  
        - Use 'analyze_sentiment' for performing sentiment analysis.  
        - Use 'compress_file' for compressing files.  
        - Use 'resize_image' for resizing images.  
        - Use 'convert_audio' for converting audio formats.  
        - Use 'fetch_api_data' for fetching data from APIs.  
        - Use 'execute_sql' for running SQL queries.  
        - Use 'send_email' for sending emails.  
        - Use 'log_activity' for logging system activities.  
        - Use 'validate_input' for input validation.  
        - Use 'hash_data' for hashing sensitive data.  
        
        Always return relative paths for system directory locations.         Example: Use './data/<file>' instead of '/data/<file>'.  
    
                """
            }
        ],
        "tools": tools,
        "tool_choice": "auto",
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"GPT query failed: {str(e)}")
```