import os
import sys

from loguru import logger

# Logger
# Here, we incorporate {process} into the default format
logger.remove()
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<red> PID {process}</red> | <level>{level: <8}</level>| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
logger.add(
    sys.stdout,
    format=log_format,
)

NOTION_PROJECT_DATABASE_ID = os.environ.get("NOTION_PROJECT_DATABASE_ID", None)
NOTION_TASK_DATABASE_ID = os.environ.get("NOTION_TASK_DATABASE_ID", None)
NOTION_TEMPS_PROJECT_DATABASE_ID = os.environ.get(
    "NOTION_TEMPS_PROJECT_DATABASE_ID", None
)
NOTION_COMPANY_DATABASE_ID = os.environ.get("NOTION_COMPANY_DATABASE_ID", None)
NOTION_PEOPLE_DATABASE_ID = os.environ.get("NOTION_PEOPLE_DATABASE_ID", None)
