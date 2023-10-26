import os
from notion_manager.notion.database.database import NotionDatabase


class NotionProjectDatabase(NotionDatabase):
    def __init__(self) -> None:
        super().__init__(database_id=os.environ.get("NOTION_PROJECT_DATABASE_ID"))
