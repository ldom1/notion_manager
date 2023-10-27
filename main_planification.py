import pandas as pd
from tqdm import tqdm
from notion_manager.config import MY_PROJECT_NAME_DICT
from notion_manager.notion.database.planification_projet_database import (
    NotionPlanificationProjectDatabase,
)
import structlog

logger = structlog.get_logger(__name__)

# Read data
logger.info("Reading data loaded from planification.xlsx...")
df = pd.read_excel("data/planification.xlsx", sheet_name="summary")
logger.info(f"Found {df.shape[0]} timeslots.")

# Filter on projects
logger.info(f"Filtering on projects: {MY_PROJECT_NAME_DICT.keys()}...")

my_project_df = df[df["project"].isin(MY_PROJECT_NAME_DICT)]

# Group by week
my_project_df_gr = my_project_df.groupby(
    ["client", "project", "username", "week"], as_index=False
)["volume"].sum()

my_project_df_gr["project_id"] = my_project_df_gr["project"].map(MY_PROJECT_NAME_DICT)
logger.info(f"Found {my_project_df_gr.shape[0]} timeslots.")

# Delete all timeslots in Notion
logger.info("Deleting all timeslots in Notion...")
NotionPlanificationProjectDatabase().delete_items_in_database()

# Add all timeslots in Notion
logger.info(f"Adding {my_project_df_gr.shape[0]} timeslots in Notion..")

for _, row in tqdm(my_project_df_gr.iterrows()):
    response = NotionPlanificationProjectDatabase().add_one_timeslot(row)
    if response.get("status", None) is not None and response.get("status", None) in [
        400,
        404,
    ]:
        print(response)
        raise Exception("Error while adding timeslot: {}".format(row))

logger.info("Done.")