import os
import requests
import agentops
from dotenv import load_dotenv

load_dotenv()
agentops.init(os.getenv("AGENTOPS_API_KEY"))

API_KEY = os.getenv("PURDUE_GENAI_API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}
payload = {"model": "llama3.2:latest", "messages": [{"role": "user", "content": "Hello!"}]}
response = requests.post("https://genai.rcac.purdue.edu/api/v1/chat/completions", headers=headers, json=payload)
