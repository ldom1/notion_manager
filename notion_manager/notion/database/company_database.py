from notion_manager import config
from notion_manager.notion.database.database import NotionDatabase


class NotionCompanyDatabase(NotionDatabase):
    def __init__(self) -> None:
        super().__init__(database_id=config.NOTION_COMPANY_DATABASE_ID)

    def get_company_name_from_id(self, company_id: str) -> str:
        """
        Get the people name from the people id
        :param people_id: People id
        :return: People name
        """
        items = self.list_items()
        for item in items:
            if item["id"] == company_id:
                return item["properties"]["Nom"]["title"][0]["text"]["content"]
        return None
