import json
import os
import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

class GeneralUtils:
    @staticmethod
    def restcountries(country, fields=[]):
        """
        retrieves information about specific country
        Example:
        restcountries('France', ['population'])
        """
        host = "https://restcountries.com/v2"

        if len(fields) == 0:
            url = host + "/name/" + country + "?fields=" + ";".join(fields)
        else:
            url = host + "/name/" + country

        response = requests.get(url=url)
        return json.loads(response.content)[0]

    @staticmethod
    def generate_meme(template_name, text, picture_link, output_file_name):
        """
        This method returns link to meme based on provided text and link to picture.
        Example: generate_meme("fancy-squirrels-hang-yearly-1157", "Gdy szef pyta, kto chętny na sobotni release.","https://a.pinatafarm.com/1210x799/bb90789ee7/puppet-monkey-looking-away.jpg", "my_meme")
        """
        host = "https://api.renderform.io/"
        endpoint = "api/v2/render"
        url = host + endpoint
        headers = {
            "x-api-key": f"{os.getenv('RENDER_FORM_API_KEY')}",
            "Content-Type": "application/json",
        }
        request_body = json.dumps(
            {
                "template": template_name,
                "data": {
                    "title.text": text,
                    "image.src": picture_link,
                },
                "fileName": output_file_name,
            }
        )
        response = requests.post(headers=headers, url=url, data=request_body)
        return response.json()["href"]

    @staticmethod
    def serpapi(query):
        """
        retrieves first snippet from serp api query to google.
        Example:
        serpapi("Who is tallest man in the world?")
        """
        params = {
            "engine": "google",
            "q": query,
            "api_key": os.getenv("SERP_API_KEY"),
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]
        return organic_results[0]["snippet"]

    @staticmethod
    def save_file_from_the_web(url, format, filename, path=""):
        response = requests.get(
            url,
            params={"downloadformat": format},
        )

        with open(f"{path}{filename}.{format}", "wb") as f:
            f.write(response.content)
