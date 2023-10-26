import os
import requests
from notion_manager.notion.database.database import NotionDatabase
from notion_manager.notion.utils import (
    NOTION_BASE_URL,
    clean_email,
    clean_metadata_creation_date,
    clean_text,
    get_headers,
)


class NotionPeopleDatabase(NotionDatabase):
    def __init__(self) -> None:
        super().__init__(database_id=os.environ.get("NOTION_PEOPLE_DATABASE_ID"))

    def list_database_properties(self):
        """
        Update date: 2023-10-01
        """
        properties = [
            "E-mail perso",
            "Date de création",
            "E-mail pro",
            "Téléphone",
            "Fonction",
            "Étiquettes",
            "Entreprise",
            "Nom",
            "Profile",
            "Linkedin",
        ]
        return properties

    def add_one_person(
        self,
        nom,
        entreprise,
        fonction,
        telephone,
        email_pro,
        email_perso,
        date_creation,
        etiquettes,
        profile,
        linkedin,
    ):
        """
        Create a new page in a Notion database
        :param database_id: The ID of the database
        :return: JSON response
        """

        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "E-mail perso": {
                    "type": "email",
                    "email": clean_email(email=email_perso),
                },
                "Date de création": {
                    "type": "date",
                    "date": {
                        "start": clean_metadata_creation_date(
                            creation_date=date_creation
                        ),
                        "end": None,
                        "time_zone": None,
                    },
                },
                "E-mail pro": {"type": "email", "email": clean_email(email=email_pro)},
                "Téléphone": {"type": "phone_number", "phone_number": telephone},
                "Fonction": {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": clean_text(text=fonction),
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
                            "plain_text": clean_text(text=fonction),
                            "href": None,
                        }
                    ],
                },
                "Étiquettes": {
                    "type": "multi_select",
                    "multi_select": [
                        {"name": clean_text(text=entreprise), "color": "red"},
                        *[{"name": tag} for tag in etiquettes],
                    ],
                },
                "Entreprise": {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": clean_text(text=entreprise),
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
                            "plain_text": clean_text(text=entreprise),
                            "href": None,
                        }
                    ],
                },
                "Profile": {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": clean_text(text=profile), "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": clean_text(text=profile),
                            "href": None,
                        }
                    ],
                },
                "Linkedin": {"type": "url", "url": clean_text(text=linkedin)},
                "Nom": {
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": clean_text(text=nom), "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": clean_text(text=nom),
                            "href": None,
                        }
                    ],
                },
            },
        }

        url = f"{NOTION_BASE_URL}/pages"
        payload = ""
        headers = get_headers()

        response = requests.request(
            "POST", url, headers=headers, data=payload, json=data
        )
        return response.json()
