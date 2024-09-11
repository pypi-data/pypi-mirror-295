import json
import os

import requests
from furl import furl


class CoderiderClient:

    def __init__(self):
        self.coderider_host = os.environ.get("CODERIDER_HOST") or "https://coderider.jihulab.com"
        self.pat = os.environ.get("AI_BOT_PERSONAL_ACCESS_TOKEN")  # GitLab PAT
        self.jwt = None  # CodeRider Server JWT

    def login(self):
        url = furl(self.coderider_host).join("api/v1/auth/jwt").url
        headers = {
            "Content-Type": "application/json",
            "PRIVATE-TOKEN": self.pat
        }
        response = requests.post(url, headers=headers)
        self.jwt = response.json()
        return self

    def chat_completions(self, messages=[], model="maas-chat-model"):
        url = furl(self.coderider_host).join("api/v1/llm/v1/chat/completions").url
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.jwt['token']}"
        }
        data = {
            "stream": False,
            "model": model,
            "messages": messages
        }

        if os.environ.get("DEBUG") == 'true':
            print(f"Request Chat completions to: {url}\n")
            print(data)
            print("\n\n-----\n\n")

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()


if __name__ == '__main__':
    client = CoderiderClient()
    client.login()
    messages = [
        {
            "role": "system",
            "content": "You are an intelligent assistant."
        },
        {
            "role": "user",
            "content": "Introduce GitLab in one sentence."
        }
    ]
    resp = client.chat_completions(messages)
    content = resp["choices"][0]["message"]["content"]
