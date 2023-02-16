import pandas as pd
import etl
from peewee import chunked
from peewee_models import *

country_code_df = pd.read_csv("../datasets/processed/codigo_pais.csv")
wdi_df = pd.read_csv(
    "../datasets/processed/world_development_indicators/world_development_indicators.csv"
)

# Renombramos y limpiamos columnas en el dataframe de WDI

wdi_df = wdi_df.rename(
    {"Country Name": "region", "Series Name": "conditions"}, axis=1
).drop(["Unnamed: 0", "Country Code"], axis=1)

j = []
for i in wdi_df.columns:
    j.append(i.split(" ")[0])
wdi_df.columns = j

# Renombramos los valores de Series Name en el dataframe de WDI

wdi_df["conditions"] = wdi_df["conditions"].str.replace("%", "percent")
wdi_df["conditions"] = wdi_df["conditions"].apply(
    etl.remove_special_characters
)
wdi_df["conditions"] = wdi_df["conditions"].str.replace(" ", "_")

# Transponemos el dataframe de WDI de manera tal que queden los años como filas y las condiciones como columnas

wdi_df = (
    wdi_df.set_index(["region", "conditions"])
    .rename_axis("year", axis=1)
    .stack()
    .unstack(1)
    .reset_index()
    .rename_axis(None, axis=1)
    .rename_axis("id")
)

etl.insert_country_code(wdi_df)
wdi_df[["region", "region_id", "year"] + etl.economia].to_csv(
    "../datasets/sql/world_development_indicators/wdi_economia.csv"
)
wdi_df[["region", "region_id", "year"] + etl.salud].to_csv(
    "../datasets/sql/world_development_indicators/wdi_salud.csv"
)
wdi_df[["region", "region_id", "year"] + etl.educacion].to_csv(
    "../datasets/sql/world_development_indicators/wdi_educacion.csv"
)
wdi_df[["region", "region_id", "year"] + etl.empleos].to_csv(
    "../datasets/sql/world_development_indicators/wdi_empleos.csv"
)
wdi_df[["region", "region_id", "year"] + etl.poblacion].to_csv(
    "../datasets/sql/world_development_indicators/wdi_poblacion.csv"
)

with database.atomic():
    for batch in chunked(wdi_df[["region", "region_id", "year"] + etl.poblacion].to_dict(orient="records"),100):
        Demography.insert_many(batch).execute()
    for batch in chunked(wdi_df[["region", "region_id", "year"] + etl.economia].to_dict(orient="records"),100):
        Economy.insert_many(batch).execute()
    for batch in chunked(wdi_df[["region", "region_id", "year"] + etl.educacion].to_dict(orient="records"),100):
        Education.insert_many(batch).execute()
    for batch in chunked(wdi_df[["region", "region_id", "year"] + etl.empleos].to_dict(orient="records"),100):
        Employment.insert_many(batch).execute()
    for batch in chunked(wdi_df[["region", "region_id", "year"] + etl.salud].to_dict(orient="records"),100):
        Health.insert_many(batch).execute()
