import json
import os
import requests


from notion_client import Client
from ai_config import TasksApiConfig

from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_HOSTNAME = TasksApiConfig.notion_hostname
NOTION_HEADER = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
}

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2021-05-13",
    "Content-Type": "application/json",
}


class NotionUtils:
    notion = Client(auth=NOTION_TOKEN)

    def create_new_note(parent_id, content):
        """
        Create a new note on Notion with the given parent_id and content.

        This function sends a POST request to the Notion API to create a new note.
        The note is created as a child of the page with the given parent_id, and
        its title is set to the given content.

        Args:
            parent_id (str): The ID of the parent page where the new note will be created. example:"12345432"
            content (str): The content to be used as the title of the new note. example:"I have 2 kids"

        Returns:
            dict: The JSON response from the Notion API, which includes details of the newly created note.
        sample usage:
        """

        url = NOTION_HOSTNAME + "pages/"
        data = json.dumps(
            {
                "parent": {"page_id": parent_id},
                "properties": {"title": {"title": [{"text": {"content": content}}]}},
            }
        )
        result = requests.post(url=url, headers=headers, data=data)
        return result.json()

    def update_existing_note(page_id, content):
        """
        :param page_id: string with page to update
        :param content: new content of page after update
        :returns: new page body
        Example:
        update_existing_note(page_id="12345, content="My favourite food is pasta")
        """
        url = NOTION_HOSTNAME + f"pages/{page_id}"
        data = json.dumps(
            {
                "properties": {"title": {"title": [{"text": {"content": content}}]}},
            }
        )
        result = requests.patch(url=url, headers=headers, data=data)
        return result.json()

    def search_notes(query):
        """
        :param query: string to search in notion
        :returns: list of results with id, content and link.
        Example:
        input:
        search_notes("yearly")
        output:
        [{'id': '2321332132',
        'content': 'Yearly Goals',
        'url': 'https://www.notion.so/Yearly-Goals-2321332132'}]
        """
        url = NOTION_HOSTNAME + "search"
        data = json.dumps(
            {
                "query": query,
            }
        )
        response = requests.post(url=url, headers=headers, data=data)
        results_list = [
            {
                "id": result["id"],
                "content": result["properties"]["title"]["title"][0]["plain_text"],
                "url": result["url"],
            }
            for result in response.json()["results"]
        ]
        return results_list
