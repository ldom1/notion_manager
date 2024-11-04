import time

import plotly.express as px
import streamlit as st

from notion_manager import mapping
from notion_manager.notion.database.people_database import NotionPeopleDatabase
from notion_manager.notion.database.planification_projet_database import (
    NotionPlanificationProjectDatabase,
)
from notion_manager.notion.database.project_database import NotionProjectDatabase
from notion_manager.notion.database.temps_projet_database import (
    NotionTempsProjectDatabase,
)

st.title("Artelys - CDP Dashboard")


# Load data
@st.cache_data
def load_data():
    """
    Load data from Notion
    """
    project_df = NotionProjectDatabase().get_df()
    people_df = NotionPeopleDatabase().get_df()
    temps_projet_df = NotionTempsProjectDatabase().get_df()
    planification_projet_df = NotionPlanificationProjectDatabase().get_df()

    temps_projet_df["Projet"] = temps_projet_df["Project"].apply(
        lambda x: mapping.MY_PROJECT_NAME_DICT[x[0]]
    )
    planification_projet_df["Projet"] = planification_projet_df["Project"].apply(
        lambda x: mapping.MY_PROJECT_NAME_DICT[x[0]]
    )

    return project_df, people_df, temps_projet_df, planification_projet_df


def merge_temps_planification(temps_projet_df, planification_projet_df):
    """
    Merge temps_projet_df and planification_projet_df
    :param temps_projet_df: DataFrame
    :param planification_projet_df: DataFrame"""

    temps_projet_df["temps_consomme"] = temps_projet_df["Volume"]
    temps_projet_df = temps_projet_df.drop(columns=["Volume"], axis=1)

    planification_projet_df["temps_planifie"] = planification_projet_df["Volume"]
    planification_projet_df = planification_projet_df.drop(columns=["Volume"], axis=1)

    df = temps_projet_df[
        ["Client", "Projet", "People", "Week", "temps_consomme"]
    ].merge(
        planification_projet_df[
            ["Client", "Projet", "People", "Week", "temps_planifie"]
        ],
        on=["Client", "Projet", "People", "Week"],
        how="outer",
    )

    df["temps_consomme"] = df["temps_consomme"].fillna(0)
    return df


project_df, people_df, temps_projet_df, planification_projet_df = load_data()
project_names = project_df["Nom du projet"].unique()
temps_df = merge_temps_planification(
    temps_projet_df=temps_projet_df, planification_projet_df=planification_projet_df
)

# Application
with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(0.1)
    project_name = st.sidebar.selectbox("Select project", project_names)

# Filter data
project_df_filter = project_df[project_df["Nom du projet"] == project_name]
temps_df = temps_df[temps_df["Projet"] == project_name]

# Main KPIs
st.header(f"Projet - {project_name}")

avancement = float(project_df_filter["Avancement projet"].iloc[0])
avancement_objectif_realise = float(
    project_df_filter["Avancement coût réalisé/objectif"].iloc[0]
)
avancement_calendaire = float(project_df_filter["Avancement calendaire"].iloc[0])
charge_totale_estimé = float(project_df_filter["[TS] Charge totale estimée"].iloc[0])
charge_totale_objectif = float(project_df_filter["[TS] Charge totale objectif"].iloc[0])
charge_restante_theorique = charge_totale_estimé * (1 - avancement)
charge_consomme = temps_df["temps_consomme"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Charge totale estimée", f"{charge_totale_estimé:.0f} jours")
col3.metric("Charge totale objectif", f"{charge_totale_objectif:.0f} jours")
col2.metric("Charge consomme", f"{charge_consomme:.0f} jours")

col1, col2, col3 = st.columns(3)
col1.metric(
    "Avancement",
    value=f"{avancement:.0%}",
    delta=f"{(avancement - avancement_objectif_realise):.0%}",
    delta_color="normal",
)
col2.metric("Avancement coût réalisé/objectif", f"{avancement_objectif_realise:.0%}")
col3.metric("Avancement calendaire", f"{avancement_calendaire:.0%}")

# Graphs
# Write bar plot to compare temps consomme vs temps planifie
st.header("Temps consommé vs temps planifié - Global")
fig = px.bar(
    temps_df,
    x="People",
    y=["temps_planifie", "temps_consomme"],
    barmode="group",
    title="Time planned vs time consumed by People",
)
st.plotly_chart(fig)

st.header("Temps consommé vs temps planifié - By week")
fig = px.bar(
    temps_df,
    x="People",
    y=["temps_planifie", "temps_consomme"],
    barmode="group",
    color="Week",
    title="Evolution of time planned vs time consumed by People",
)
st.plotly_chart(fig)
