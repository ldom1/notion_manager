import pandas as pd
import requests
from dotenv import find_dotenv, load_dotenv
from tqdm import tqdm

from notion_manager import config
from notion_manager.notion.utils import NOTION_BASE_URL, get_headers

load_dotenv(find_dotenv())


class NotionDatabase:
    def __init__(self, database_id) -> None:
        self.database_id = database_id

    def __name__(self):
        return self.__class__.__name__

    @staticmethod
    def check_property_exists(row, property):
        """
        Check if a property exists in a Notion database
        :param row: The row to check
        :param property: The property to check

        :return: True if the property exists, False otherwise
        """

        if isinstance(row, dict):
            if property in row:
                return True
            else:
                return False

        elif isinstance(row, pd.Series):
            if property in row.index:
                return True
            else:
                return False

    def list_items(self) -> list:
        """
        List all items in a Notion database
        :param database_id: The ID of the database
        :return: result
        """
        url = f"{NOTION_BASE_URL}/databases/{self.database_id}/query"
        payload = ""
        headers = get_headers()

        page_size = 100
        payload = {"page_size": page_size}

        results = []
        has_more = True

        while has_more:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            results.extend(data["results"])
            has_more = data["has_more"]
            if has_more:
                payload["start_cursor"] = data["next_cursor"]

        return results

    def list_database_properties_from_item(self):
        """
        List all properties in a Notion database
        :param database_id: The ID of the database
        :return: JSON response
        """

        items = self.list_items()
        return list(items[0]["properties"].keys()) if items else list()

    def delete_item(self, item_id):
        """
        Delete items in a Notion database
        :param database_id: The ID of the database
        :param item_id: The IDs of the item to delete
        :return: JSON response
        """
        url = f"{NOTION_BASE_URL}/blocks/{item_id}"
        headers = get_headers()

        response = requests.request("DELETE", url, headers=headers)
        return response.json()

    def delete_items_in_database(self):
        """
        Delete items in a Notion database
        :param database_id: The ID of the database
        :return: JSON response
        """
        items = self.list_items()

        if not items:
            return False

        elif len(items) == 0:
            return False

        else:
            for item in tqdm(items):
                self.delete_item(item_id=item["id"])
            return True

    def get_df_items(self) -> pd.DataFrame:
        """
        Get all items in a Notion database as a pandas DataFrame
        :return: pandas DataFrame
        """
        items = self.list_items()

        if not items:
            return pd.DataFrame()
        elif len(items) == 0:
            return pd.DataFrame()
        else:
            df = pd.DataFrame([y["properties"] for y in items])
            return df

    def get_df(self) -> pd.DataFrame:
        """
        Clean a pandas DataFrame
        :param df: pandas DataFrame to clean
        :return: Cleaned pandas DataFrame
        """
        df = self.get_df_items()

        for col in df.columns:
            try:
                df[col] = df[col].apply(
                    lambda x: NotionDatabase.get_value_from_property(x)
                )
            except Exception as e:
                config.logger.error(
                    f"""
                    Error while cleaning column {col}: {e} with Database {self.__name__()}.
                    Example of df columns to clean:
                    {df.head(3)[col]}
                    """
                )
        return df

    @staticmethod
    def get_value_from_property(property_dict: dict) -> str:
        """
        :param property_dict: A dictionary of a Notion property

        """
        try:
            if "title" in property_dict:
                title = property_dict["title"]
                if len(title) > 0:
                    return title[0]["plain_text"]
                else:
                    return None
            elif "rich_text" in property_dict:
                rich_text = property_dict["rich_text"]
                if len(rich_text) > 0:
                    return rich_text[0]["plain_text"]
                else:
                    return None
            elif "number" in property_dict:
                return property_dict["number"]
            elif "select" in property_dict:
                return property_dict["select"]["name"]
            elif "multi_select" in property_dict:
                return [x["name"] for x in property_dict["multi_select"]]
            elif "date" in property_dict:
                if property_dict["date"] is None:
                    return None
                else:
                    return property_dict["date"]["start"]
            elif "formula" in property_dict:
                if property_dict["formula"]["type"] == "string":
                    return property_dict["formula"]["string"]
                elif property_dict["formula"]["type"] == "number":
                    return property_dict["formula"]["number"]
                else:
                    return None
            elif "relation" in property_dict:
                return [x["id"] for x in property_dict["relation"]]
            elif "rollup" in property_dict:
                return property_dict["rollup"]["number"]
            else:
                return None
        except IndexError or KeyError:
            raise Exception(f"Could not get value from property: {property_dict}")
