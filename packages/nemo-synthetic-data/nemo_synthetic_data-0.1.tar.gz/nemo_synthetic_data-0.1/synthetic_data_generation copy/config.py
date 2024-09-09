import requests

class CustomClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def chat_completion(self, model, messages, temperature=0.7, top_p=1.0):
        url = f"{self.base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self.api_key != "none":
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

def get_client(base_url, api_key, model):
    return CustomClient(base_url, api_key), model