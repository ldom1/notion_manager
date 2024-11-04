from datetime import datetime
from typing import Dict

import pandas as pd

import notion_manager.mapping
from notion_manager import config


def get_filtered_df(df: pd.DataFrame) -> pd.DataFrame:
    dfs = []

    for _, project in notion_manager.mapping.MY_PROJECT_NAME_DICT.items():
        config.logger.info(
            f"Filtering DF: Considering project: {project['name']} - {project['task']}"
        )
        if project["task"] == "all":
            dfs.append(df[df["project"] == project["name"]])
        else:
            dfs.append(
                df[(df["project"] == project["name"]) & (df["task"] == project["task"])]
            )

    return pd.concat(dfs)


def process_forecasts_summary(
    forecasts_summary: pd.DataFrame, mapping_prj: Dict[str, str]
) -> pd.DataFrame:
    # Filter the DataFrame
    forecasts_summary_project = forecasts_summary[
        forecasts_summary["Related project or concerned activity"]
        == mapping_prj["timesheet_name"]
    ].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Convert Date Monday to datetime
    forecasts_summary_project.loc[:, "Date Monday"] = pd.to_datetime(
        forecasts_summary_project["Date Monday"]
    )
    forecasts_summary_project["Year"] = forecasts_summary_project["Date Monday"].dt.year
    forecasts_summary_project["Month"] = forecasts_summary_project[
        "Date Monday"
    ].dt.month

    # Extract week number
    forecasts_summary_project["Week"] = (
        forecasts_summary_project["Date Monday"].dt.isocalendar().week
    )
    forecasts_summary_project["Page name"] = (
        forecasts_summary_project["Client (if project)"].astype(str)
        + " - "
        + forecasts_summary_project["Related project or concerned activity"].astype(str)
        + " - "
        + forecasts_summary_project["Name"].astype(str)
        + " - "
        + "W"
        + forecasts_summary_project["Week"].astype(str)
    )

    # Convert project in notion project name
    forecasts_summary_project["Project"] = mapping_prj["notion_name"]

    return forecasts_summary_project


def process_realise_summary(
    realise_summary: pd.DataFrame, mapping_prj: Dict[str, str]
) -> pd.DataFrame:
    realise_summary_project = realise_summary[
        realise_summary["project"] == mapping_prj["timesheet_name"]
    ].copy()

    # Convert number to integer
    realise_summary_project["year"] = pd.to_numeric(
        realise_summary_project["year"], downcast="integer"
    )
    realise_summary_project["month"] = pd.to_numeric(
        realise_summary_project["month"], downcast="integer"
    )
    realise_summary_project["week"] = pd.to_numeric(
        realise_summary_project["week"], downcast="integer"
    )

    # Convert volume to float
    realise_summary_project["volume"] = pd.to_numeric(
        realise_summary_project["volume"], downcast="float"
    )

    # Add project name & page name
    realise_summary_project["project"] = mapping_prj["notion_name"]
    realise_summary_project["page_name"] = (
        realise_summary_project["client"].astype(str)
        + " - "
        + realise_summary_project["project"].astype(str)
        + " - "
        + realise_summary_project["username"].astype(str)
        + " - "
        + "W"
        + realise_summary_project["week"].astype(str)
    )

    # Adapt the month column based on the year and week
    realise_summary_project["month"] = realise_summary_project.apply(
        lambda x: get_month_from_year_and_week(year=x["year"], week=x["week"]), axis=1
    )

    # Group by to get the volume per page_name, client, project, username, year, month, week
    realise_summary_project = (
        realise_summary_project.groupby(
            ["page_name", "client", "project", "username", "year", "month", "week"]
        )
        .agg({"volume": "sum"})
        .reset_index()
    )

    # Round the volume to 2 decimals
    realise_summary_project["volume"] = realise_summary_project["volume"].round(2)

    return realise_summary_project


def get_month_from_year_and_week(year: int, week: int) -> int:
    # Get the Monday of the given week
    first_day_of_week = datetime.strptime(f"{year} {week} 1", "%G %V %u")
    # Get the month
    month = first_day_of_week.month
    return month
