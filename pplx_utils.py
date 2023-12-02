import os
import requests

from ai_config import TasksApiConfig

from dotenv import load_dotenv

load_dotenv()

PPLX_API_TOKEN = os.getenv("PPLX_API_TOKEN", "")
PPLX_API_HOSTNAME = TasksApiConfig.pplx_api_hostname
PPLX_API_HEADER = {
    "Authorization": f"Bearer {PPLX_API_TOKEN}",
    "accept": "application/json",
    "Content-Type": "application/json",
}


class PplxApi:
    def pplx_chat_completions(
        model,
        system_message,
        user_message,
    ):
        url = PPLX_API_HOSTNAME
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        }
        response = requests.post(url=url, json=payload, headers=PPLX_API_HEADER)
        return response.json()["choices"][0]["message"]["content"]
