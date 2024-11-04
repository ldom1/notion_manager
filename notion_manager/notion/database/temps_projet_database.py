import json
from typing import Optional

import pandas as pd
import requests

from notion_manager import config
from notion_manager.notion.database.company_database import NotionCompanyDatabase
from notion_manager.notion.database.database import NotionDatabase
from notion_manager.notion.database.people_database import NotionPeopleDatabase
from notion_manager.notion.database.project_database import NotionProjectDatabase
from notion_manager.notion.utils import (
    NOTION_BASE_URL,
    get_headers,
    get_id_from_name,
    get_name_from_id,
)


class NotionTempsProjectDatabase(NotionDatabase):
    def __init__(self) -> None:
        super().__init__(database_id=config.NOTION_TEMPS_PROJECT_DATABASE_ID)

        self.company_db_items = NotionCompanyDatabase().list_items()
        self.people_db_items = NotionPeopleDatabase().list_items()
        self.project_db_items = NotionProjectDatabase().list_items()

        self.temps_project_items = self.list_items()

    def get_df(self):
        data = []

        for item in self.temps_project_items:
            row = {
                "id": item["id"],
                "Client": get_name_from_id(
                    items=self.company_db_items,
                    id=item["properties"]["Client"]["relation"][0]["id"],
                ),
                "Projet": get_name_from_id(
                    items=self.project_db_items,
                    id=item["properties"]["Project"]["relation"][0]["id"],
                ),
                "People": get_name_from_id(
                    items=self.people_db_items,
                    id=item["properties"]["People"]["relation"][0]["id"],
                ),
                "Year": item["properties"]["Year"]["number"],
                "Month": item["properties"]["Month"]["number"],
                "Week": item["properties"]["Week"]["number"],
                "volume_realise": item["properties"]["Volume réalisé"]["number"],
                "volume_prevu": item["properties"]["Volume planifié"]["number"],
            }
            data.append(row)

        df = pd.DataFrame(data)
        return df

    def get_page_id_in_notion(
        self, client: str, project: str, username: str, year: int, month: int, week: int
    ) -> Optional[str]:
        """
        Check if a timeslot exists in the database
        :param client: Client name
        :param project: Project name
        :param username: Username
        :param year: Year
        :param month: Month
        :param week: Week
        :return: page_id (str) or None
        """
        df_temps_projet = self.get_df()
        df_temps_projet_filtered = df_temps_projet[
            (df_temps_projet["Client"] == client)
            & (df_temps_projet["Projet"] == project)
            & (df_temps_projet["People"] == username)
            & (df_temps_projet["Year"] == year)
            & (df_temps_projet["Month"] == month)
            & (df_temps_projet["Week"] == week)
        ]

        if df_temps_projet_filtered.empty:
            return None
        if df_temps_projet_filtered.shape[0] > 1:
            raise ValueError("Multiple timeslots found")
        return df_temps_projet_filtered.iloc[0]["id"]

    def add_one_timeslot(
        self,
        page_name: str,
        client: str,
        project: str,
        username: str,
        year: int,
        month: int,
        week: int,
        volume_planifie: Optional[int] = 0,
        volume_realise: Optional[int] = 0,
        task: Optional[str] = "Réalisation",
    ):
        """
        Add a new timeslot to the database
        :param page_name: Page name
        :param client: Client name
        :param project: Project name
        :param username: Username
        :param year: Year
        :param month: Month
        :param week: Week
        :param task: Task
        :param volume_planifie: Planned volume
        :param volume_realise: Realized volume
        :return: dict (Notion response)
        """
        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Client": {
                    "type": "relation",
                    "relation": [
                        {
                            "id": get_id_from_name(
                                items=self.company_db_items,
                                name=client,
                            )
                        }
                    ],
                    "has_more": False,
                },
                "Project": {
                    "type": "relation",
                    "relation": [
                        {
                            "id": get_id_from_name(
                                items=self.project_db_items,
                                name=project,
                            )
                        }
                    ],
                    "has_more": False,
                },
                "People": {
                    "type": "relation",
                    "relation": [
                        {
                            "id": get_id_from_name(
                                items=self.people_db_items,
                                name=username,
                            )
                        }
                    ],
                },
                "Nom": {
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": page_name, "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": page_name,
                            "href": None,
                        }
                    ],
                },
                "Year": {"type": "number", "number": year},
                "Month": {"type": "number", "number": month},
                "Week": {"type": "number", "number": week},
                "Volume réalisé": {"type": "number", "number": volume_realise},
                "Volume planifié": {"type": "number", "number": volume_planifie},
                "Task": {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": task,
                                "link": None,
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": task,
                            "href": None,
                        }
                    ],
                },
            },
        }

        url = f"{NOTION_BASE_URL}/pages"
        payload = json.dumps(data)
        headers = get_headers()

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code != 200:
            raise ValueError(response.text)
        return response.json()

    def update_one_timeslot(
        self,
        page_id: str,
        volume_planifie: Optional[int] = None,
        volume_realise: Optional[int] = None,
        task: Optional[str] = None,
    ):
        """
        Update a timeslot in the database
        :param row: dict (client, project, username, volume, week) from the csv file loaded using pandas DataFrame
        :return: dict (Notion response)
        """
        data = {
            "properties": {},
        }
        if not volume_planifie and not volume_realise and not task:
            return None
        if volume_planifie:
            data["properties"]["Volume planifié"] = {
                "type": "number",
                "number": volume_planifie,
            }

        if volume_realise:
            data["properties"]["Volume réalisé"] = {
                "type": "number",
                "number": volume_realise,
            }

        if task:
            data["properties"]["Task"] = {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": task,
                            "link": None,
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": task,
                        "href": None,
                    }
                ],
            }

        url = f"{NOTION_BASE_URL}/pages/{page_id}"
        payload = json.dumps(data)
        headers = get_headers()

        response = requests.request("PATCH", url, headers=headers, data=payload)

        if response.status_code != 200:
            raise ValueError(response.text)
        return response.json()

    def create_or_update_one_timeslot(
        self,
        page_name: str,
        client: str,
        project: str,
        username: str,
        year: int,
        month: int,
        week: int,
        task: Optional[str] = "Réalisation",
        volume_planifie: Optional[int] = 0,
        volume_realise: Optional[int] = 0,
    ):
        """
        Create or update a timeslot in the database
        :param row: dict (client, project, username, volume, week) from the csv file loaded using pandas DataFrame
        :return: dict (Notion response)
        """
        page_id = self.get_page_id_in_notion(
            client=client,
            project=project,
            username=username,
            year=year,
            month=month,
            week=week,
        )

        if page_id:
            config.logger.info(f"Updating timeslot {page_name}")
            self.update_one_timeslot(
                page_id=page_id,
                volume_planifie=volume_planifie,
                volume_realise=volume_realise,
                task=task,
            )

        else:
            config.logger.info(f"Creating timeslot {page_name}")
            self.add_one_timeslot(
                page_name=page_name,
                client=client,
                project=project,
                username=username,
                year=year,
                month=month,
                week=week,
                task=task,
                volume_planifie=volume_planifie,
                volume_realise=volume_realise,
            )
