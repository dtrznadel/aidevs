import json


class TasksApiConfig:
    endpoint = "https://zadania.aidevs.pl"
    task_hostname = "https://zadania.aidevs.pl"

    task_name = "scraper"
    body_apikey = json.dumps({"apikey": "b47e0620-c5cf-451f-a8d3-be670584d9f2"})

    openai_hostname = "https://api.openai.com/v1/"
    openai_endpoint = "whoami"
    default_recording_path = (
        "C:\\Users\\Dominik Trznadel\\OneDrive\Dokumenty\\Nagrania dźwiękowe\\"
    )
    google_api_hostname = "https://photoslibrary.googleapis.com/v1/"
