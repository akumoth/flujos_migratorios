import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(layout="wide")

educacion_df = pd.read_parquet("parquet/educacion_df.csv")
region_df = pd.read_parquet("parquet/region_df.csv")
migration_df = pd.read_parquet("parquet/migration_df.csv")

region_df.index = np.arange(1, len(region_df) + 1)
region_df.reset_index(inplace=True)
region_df = region_df.rename({"index": "region_id"}, axis=1)
educacion_df = educacion_df.rename({"region": "region_id"}, axis=1)

data_merge = pd.merge(educacion_df, region_df, on="region_id")
current_view = data_merge

filter1, filter2 = st.sidebar.columns(2)
with filter1:
    topicfilter = st.checkbox("Selección de países atípicos")
with filter2:
    levelfilter = st.checkbox("Habilitar filtro según nivel")

if topicfilter == True:
    current_view = current_view[current_view.name.isin(['colombia','pakistan','turkey','spain','italy','venezuela'])]

current_view.fillna(value=np.nan, inplace=True)
average_internet_users = round(
    current_view[current_view.internet_users_per_100_people != 0.0]
    .groupby("name")["internet_users_per_100_people"]
    .sum()
    .mean(),
    3,
)

bachelor_attainment = (
    current_view
    .groupby(['name','year'])['technicians_in_rd_per_million_people']
    .mean()
    .reset_index()
    .sort_values(by='year')
)
bachelor_attainment2 = pd.DataFrame(index=bachelor_attainment.year.unique(),columns=current_view.name.unique())
for i in bachelor_attainment2.columns:
    bachelor_attainment2[i] = bachelor_attainment[bachelor_attainment['name'] == i].set_index('year')['technicians_in_rd_per_million_people']
print(bachelor_attainment)
st.line_chart(bachelor_attainment2)
st.metric(
    "Numero de promedio de usuarios de internet en los paises (por cada 100 personas)",
    average_internet_users,
)
