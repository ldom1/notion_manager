import datetime
import os
import re
from typing import Any, Dict

from notion_manager import mapping

NOTION_BASE_URL = "https://api.notion.com/v1"


def get_headers() -> dict:
    """
    Get the headers for the Notion API
    :return: Dictionary of headers
    """
    return {
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22",
        "Authorization": f'Bearer {os.environ.get("NOTION_API_KEY", None)}',
    }


def clean_metadata_creation_date(creation_date: str) -> str:
    """
    Clean the creation date from the metadata
    :param creation_date: Creation date from the metadata
    :return: Cleaned creation date
    """
    if creation_date is None:
        creation_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+02:00")
    elif re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", creation_date) is not None:
        creation_date = datetime.datetime.strptime(
            creation_date, "%Y-%m-%d %H:%M"
        ).strftime("%Y-%m-%dT%H:%M:%S.000+02:00")
    elif re.match(r"\d{4}-\d{2}-\d{2}", creation_date) is not None:
        creation_date = datetime.datetime.strptime(creation_date, "%Y-%m-%d").strftime(
            "%Y-%m-%dT%H:%M:%S.000+02:00"
        )
    else:
        creation_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+02:00")
    return creation_date


def is_valid_email(email: str) -> bool:
    """
    Check if the email is valid
    :param email: Email to check
    :return: True if the email is valid, False otherwise
    """
    # Regular expression for a simple email validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def clean_email(email: str) -> str:
    """
    Clean the email
    :param email: Email to clean
    :return: Cleaned email
    """
    if is_valid_email(email):
        return email
    else:
        return None


def clean_text(text: str) -> str:
    """
    Clean the text
    :param text: Text to clean
    :return: Cleaned text
    """
    if text is None:
        return None
    elif text.strip() == "":
        return None
    else:
        return text.strip()


def get_timesheet_project_name_from_notion_project_id(project_id: str) -> str:
    """
    Get the project name from the project id
    :param project_id: Project id
    :return: Project name
    """
    for _, project_dict in mapping.MY_PROJECT_NAME_DICT.items():
        if project_dict["notion_id"] == project_id:
            return mapping.MY_PROJECT_NAME_DICT[project_dict]["timesheet_name"]
    return None


def get_name_value(dictionary):
    name_keys = ["Nom", "Name", "Nom du projet"]
    for key in name_keys:
        if key in dictionary:
            return dictionary[key]
    return None  # Return None if no matching key is found


def get_name_from_id(items: Dict[str, Any], id: str) -> str:
    """
    Get the name from the id
    :param items: List of items
    :param id: Id to search
    :return: Name
    """
    for item in items:
        if item["id"] == id:
            item_properties_name = get_name_value(dictionary=item["properties"])
            if item_properties_name is not None:
                return item_properties_name["title"][0]["text"]["content"]
    return None


def get_id_from_name(items: Dict[str, Any], name: str) -> str:
    """
    Get the id from the name
    :param items: List of items
    :param name: Name to search
    :return: Id
    """
    for item in items:
        item_properties_name = get_name_value(dictionary=item["properties"])
        if item_properties_name is not None:
            if item_properties_name["title"][0]["text"]["content"] == name:
                return item["id"]
    return None
