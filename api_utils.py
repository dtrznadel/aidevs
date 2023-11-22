
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

def openai_vision(message):
    """
        Call GPT 4V model.
        :message: Message is in ChatML (Chat Markup Language) syntax.
        Sample input syntax:
        [
        {
            "role": "system",
            "content": [{"type": "text", "text": "you are helpful assistant"}],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe the image below."},
                {
                    "type": "image_url",
                    "image_url": *your url*,
                },
            ],
        },
    ]
    :returns: model response content.

    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4-vision-preview", messages=message, max_tokens=200
    )
    return response.choices[0].message.content

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
