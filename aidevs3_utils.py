import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()
aidevs3_api_key = os.getenv("AIDEVS3_API_KEY")


class AIDevs3Utils:
    def request_authorization(task):
        data = f'{{"apikey": "{aidevs3_api_key}"}}'
        response = requests.post(
            f"https://zadania.aidevs.pl/token/{task}", data=data
        )
        response_dict = json.loads(response.text)
        # optional - print all keys
        # for i in auth_dict:
        #     print("key: ", i, "val: ", auth_dict[i])
        return response_dict["token"]

    def get_data(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def verify_results(task, answer):
        url = "https://poligon.aidevs.pl/verify"
        payload = {"task": task, "apikey": aidevs3_api_key, "answer": answer}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()


# token = request_authorization("helloapi", aidevs3_api_key)
