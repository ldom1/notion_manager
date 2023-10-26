import time
import streamlit as st
from notion_manager.config import MY_PROJECT_NAME_INVERSE_DICT

from notion_manager.notion.database.people_database import NotionPeopleDatabase
from notion_manager.notion.database.temps_projet_database import NotionTempsProjectDatabase
from notion_manager.notion.database.project_database import NotionProjectDatabase

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

    temps_projet_df["Projet"] = temps_projet_df["Project"].apply(lambda x: MY_PROJECT_NAME_INVERSE_DICT[x[0]])

    return project_df, people_df, temps_projet_df

project_df, people_df, temps_projet_df = load_data()
project_names = project_df["Nom du projet"].unique()

# Application
with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(0.1)
    project_name = st.sidebar.selectbox("Select project", project_names)

# Filter data
project_df_filter = project_df[project_df["Nom du projet"] == project_name]
temps_projet_df = temps_projet_df[temps_projet_df["Projet"] == project_name]


# Main KPIs
st.header(f"Projet - {project_name}")

avancement = float(project_df_filter["Avancement projet"].iloc[0])
avancement_objectif_realise = float(project_df_filter["Avancement coût réalisé/objectif"].iloc[0])
charge_totale_estimé = float(project_df_filter["[TS] Charge totale estimée"].iloc[0])
charge_totale_objectif = float(project_df_filter["[TS] Charge totale objectif"].iloc[0])
charge_restante_theorique = charge_totale_estimé * (1 - avancement)
charge_consomme = temps_projet_df["Volume"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Charge totale estimée", f"{charge_totale_estimé:.0f} jours")
col3.metric("Charge totale objectif", f"{charge_totale_objectif:.0f} jours")
col2.metric("Charge consomme", f"{charge_consomme:.0f} jours")

col1, col2, col3 = st.columns(3)
col1.metric("Avancement", value=f"{avancement:.0%}", delta=f"{(avancement - avancement_objectif_realise):.0%}", delta_color="normal")
col2.metric("Avancement coût réalisé/objectif", f"{avancement_objectif_realise:.0%}")
# Graphs
