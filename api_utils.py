import json
import requests

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
