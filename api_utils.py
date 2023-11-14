
import json
import openai
import os
import requests

from dotenv import load_dotenv
from serpapi import GoogleSearch

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

def call_openai_function(messages, tools):
    """
    potential further transformation to extract arguments to the first called function:
    json.loads(ai_function[0].arguments.encode("utf-8").decode("unicode_escape"))
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    result = []
    for tool_call in response.choices[0].message.tool_calls:
        result.append(tool_call.function)
    return result
