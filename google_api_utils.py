import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
from ai_config import TasksApiConfig

class GoogleApiUtils:
    @staticmethod
    def check_google_token():
        SCOPES = [
            "https://www.googleapis.com/auth/photoslibrary",
            "https://www.googleapis.com/auth/drive.metadata.readonly",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.photos.readonly",
        ]
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "google_python_project_API.json",
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    @staticmethod
    def get_photo_ids_based_on_date_range(start_date, end_date, pageSize=10):
        """
        Sample usage:
            get_photo_ids_based_on_date_range(
                start_date="2023-11-05", end_date="2023-11-06", pageSize=2
            )
        """
        GoogleApiUtils.check_google_token()
        with open("google_python_project_API.json") as secret:
            data = json.load(secret)
            oAuthclientID = data["installed"]["client_id"]
            oAuthclientSecret = data["installed"]["client_secret"]
            oAuthrefreshToken = data["installed"]["token_uri"]
            oAuthrefreshToken = data["installed"]["token_uri"]

        token = None
        with open("token.json") as secret:
            data = json.load(secret)
            token = data["token"]

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        hostname = TasksApiConfig.google_api_hostname
        search_path = "mediaItems:search"
        url = hostname + search_path
        body = {
            "pageSize": pageSize,
            "filters": {
                "dateFilter": {
                    "ranges": [
                        {
                            "startDate": {
                                "year": int(start_date.split("-")[0]),
                                "month": int(start_date.split("-")[1]),
                                "day": int(start_date.split("-")[2]),
                            },
                            "endDate": {
                                "year": int(end_date.split("-")[0]),
                                "month": int(end_date.split("-")[1]),
                                "day": int(end_date.split("-")[2]),
                            },
                        }
                    ]
                }
            },
        }
        response = requests.post(url=url, headers=headers, json=body)
        if response.status_code != 200:
            return print(
                "Request failed. Status_code: "
                + response.status_code
                + ". Content: "
                + response.content
            )
        else:
            results = response.json().get("mediaItems", [])
            sorted_results = sorted(
                results, key=lambda k: k["mediaMetadata"]["creationTime"]
            )
            ids = []
            for result in sorted_results:
                ids.append(result["id"])
        return ids

    @staticmethod
    def find_photo_google_details_based_on_id(photo_id):
        """
            sample usage
        find_photo_google_details_based_on_id(
        "AD9e7BBrkyA6SIMNkeXcS3dg3musegAntCuo3cEwuR7HDMjrQuiHRtBI3B2zxkJugi5PRYJicl8jxhpA0nRPlqhbqtVOvoVZjw"
        )
        """
        hostname = TasksApiConfig.google_api_hostname
        search_path = "mediaItems"
        with open("token.json") as secret:
            data = json.load(secret)
            token = data["token"]

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            url=hostname + search_path + "/" + photo_id, headers=headers
        )
        results = response.json()
        return results
