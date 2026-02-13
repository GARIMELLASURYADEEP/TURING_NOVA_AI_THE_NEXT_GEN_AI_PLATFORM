import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"API Key found: {bool(api_key)}")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

data = {
    "model": "stepfun/step-3.5-flash:free",
    "messages": [
        {"role": "user", "content": "Print 'Hello OpenRouter' in Python."}
    ]
}

try:
    print("Sending request to OpenRouter...")
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response Success!")
        print(response.json()['choices'][0]['message']['content'])
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
