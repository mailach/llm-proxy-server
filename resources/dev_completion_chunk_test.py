import requests
import json
import os

data = {
  "model" : "gpt-4o-mini-2024-07-18",  
  "messages": [{"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Give me the year as json"}],
  "stream": False, 
  "response_format":{"type": "json_object"}
}
url = "http://127.0.0.1:5000/chat/completions"
api_key = os.environ.get("ADMIN_API_KEY")

req = requests.post(url, headers={'Authorization': "Bearer " + api_key}, json=data)
print(req.text)
print(req.headers)