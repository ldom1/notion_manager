import json
import os

import requests
from notion_manager.notion.database.database import NotionDatabase
from notion_manager.notion.utils import NOTION_BASE_URL, get_headers


class NotionPlanificationProjectDatabase(NotionDatabase):
    def __init__(self) -> None:
        super().__init__(database_id=os.environ.get("NOTION_PLANIFICATION_PROJECT_DATABASE_ID"))

    def add_one_timeslot(self, row):
        """
        Add a new timeslot to the database
        :param row: dict (client, project, username, volume, week) from the csv file loaded using pandas DataFrame
        :return: dict (Notion response)
        """

        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Client": {
                    "type": "rich_text",
                    "rich_text": [{"type": "text", "text": {"content": row["client"]}}],
                },
                "Project": {
                    "type": "relation",
                    "relation": [{"id": row["project_id"]}],
                    "has_more": False,
                },
                "People": {
                    "type": "rich_text",
                    "rich_text": [
                        {"type": "text", "text": {"content": row["username"]}}
                    ],
                },
                "Volume": {"type": "number", "number": row["volume"]},
                "Week": {"type": "number", "number": row["week"]},
                "Étiquettes": {
                    "type": "multi_select",
                    "multi_select": [
                        {
                            "name": "temps",
                        },
                        {
                            "name": "artelys",
                        },
                    ],
                },
            },
        }

        url = f"{NOTION_BASE_URL}/pages"
        payload = json.dumps(data)
        headers = get_headers()

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
