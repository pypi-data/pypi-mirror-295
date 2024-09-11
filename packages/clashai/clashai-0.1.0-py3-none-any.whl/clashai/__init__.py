__version__ = "0.1.0"

import requests

class Client:
    def __init__(self, api_key: str, model: str = None, base_url: str = None):
        self.api_key = api_key
        self.model = model
        self.base_url =  base_url if base_url else "http://clashai.us.to"

    def make_request(self, messages: list):
        model = self.model if self.model else "chatgpt-4o-latest"
        api_key = self.api_key
        endpoint = "v1/chat/completions"
        url = f"{self.base_url}/{endpoint}"
        payload = {
                "model": model,
                "messages": messages
                                                                ,
            }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

def get_usage(id: int, base_url: str = None):
        endpoint = f"my_stats/{id}"
        base = base_url if base_url else "http://clashai.us.to"
        url = f"{base}/{endpoint}"
        response = requests.get(url)
        return response.json()