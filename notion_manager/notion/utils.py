import os
import datetime
import re

NOTION_BASE_URL = "https://api.notion.com/v1"


def get_headers():
    """
    Get the headers for the Notion API
    :return: Dictionary of headers
    """
    return {
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22",
        "Authorization": f'Bearer {os.environ.get("NOTION_API_KEY", None)}',
    }


def clean_metadata_creation_date(creation_date):
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


def is_valid_email(email):
    """
    Check if the email is valid
    :param email: Email to check
    :return: True if the email is valid, False otherwise
    """
    # Regular expression for a simple email validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def clean_email(email):
    """
    Clean the email
    :param email: Email to clean
    :return: Cleaned email
    """
    if is_valid_email(email):
        return email
    else:
        return None


def clean_text(text):
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
