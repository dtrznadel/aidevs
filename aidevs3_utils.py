import requests
import json
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
aidevs3_api_key = os.getenv("AIDEVS3_API_KEY")
domain = os.getenv("AIDEVS3_DOMAIN")


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

    def retrieve_from_html(html_content, id):
        soup = BeautifulSoup(html_content, "html.parser")
        question_element = soup.find(id=id)
        return question_element.text.strip()

    def verify_results(
        task, answer, endpoint=f"https://centrala.{domain}/report"
    ):
        payload = {"task": task, "apikey": aidevs3_api_key, "answer": answer}
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, headers=headers, json=payload)
        #        response.raise_for_status()
        return response.json()


# token = request_authorization("helloapi", aidevs3_api_key)
