import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

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
