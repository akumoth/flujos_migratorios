import pandas as pd
import numpy as np
import etl

wdi_df = pd.read_csv(
    "../datasets/processed/world_development_indicators/P-world_development_indicators.csv"
).drop('region_id',axis=1)

wdi_salud_indicador_df = pd.read_csv(
    "../datasets/processed/work_bank/indicador_de_salud_normalizado.csv"
).drop('Unnamed: 0', axis=1)

wdi_educacion_indicador_df = pd.read_csv(
    "../datasets/processed/work_bank/indicador_educacion_normalizado.csv"
).drop('Unnamed: 0', axis=1)

wdi_salud_indicador_df['Country Name'] = wdi_salud_indicador_df['Country Name'].str.lower()
wdi_salud_indicador_df['Series Name'] = wdi_salud_indicador_df['Series Name'].str.lower()

wdi_educacion_indicador_df['Country Name'] = wdi_educacion_indicador_df['Country Name'].str.lower()
wdi_educacion_indicador_df['Series'] = wdi_educacion_indicador_df['Series'].str.lower()

wdi_df = wdi_df.rename(
    {"Country name": "name", "Series Name": "conditions"}, axis=1
)

j = []
for i in wdi_df.columns:
    j.append(i.split(" ")[0])
wdi_df.columns = j

wdi_salud_indicador_df = wdi_salud_indicador_df.rename(
    {"Country Name": "name", "Series Name": "conditions"}, axis=1
)

j = []
for i in wdi_salud_indicador_df.columns:
    j.append(i.split(" ")[0])
wdi_salud_indicador_df.columns = j

wdi_educacion_indicador_df = wdi_educacion_indicador_df.rename(
    {"Country Name": "name", "Series": "conditions"}, axis=1
)

j = []
for i in wdi_educacion_indicador_df.columns:
    j.append(i.split(" ")[0])
wdi_educacion_indicador_df.columns = j

wdi_df = pd.concat([wdi_df,wdi_educacion_indicador_df,wdi_salud_indicador_df]).replace([np.nan], [None]).replace([0.0], [None])

# Renombramos y limpiamos columnas en el dataframe de WDI

wdi_df = wdi_df.reset_index(drop=True).drop('Unnamed:',axis=1)

# Transponemos el dataframe de WDI de manera tal que queden los años como filas y las condiciones como columnas

wdi_df = (
    wdi_df.set_index(["name", "conditions"])
    .rename_axis("year", axis=1)
    .stack()
    .drop_duplicates()
    .unstack(1)
    .sort_values(['name','year'])
    .reset_index()
    .rename_axis(None, axis=1)
    .rename_axis("id")
)

wdi_columns = wdi_df.columns.to_series()
wdi_columns = wdi_columns.str.lower()
wdi_columns = etl.normalize_lists(wdi_columns)
wdi_df.columns = wdi_columns

# Normalizamos los nombres de los países 

wdi_df['name'] = wdi_df['name'].apply(etl.normalize_country).str.lower()
etl.insert_country_code(wdi_df)

# Borramos los países que no esten en nuestra lista de valores a contemplar 

wdi_df.drop(wdi_df.where(~wdi_df.name.isin(etl.country_code_df['name'])).dropna().index,axis=0)
wdi_df.replace(np.nan,None,inplace=True)
wdi_df.replace(0.0,None,inplace=True)

# Generamos los archivos CSV, dividiendo la información según las tablas planteadas para la base de datos.

wdi_df[["name", "region_id", "year"] + list(set(wdi_df.columns.str.lower().to_list()) & set(etl.economia))].to_csv(
    "../datasets/sql/world_development_indicators/wdi_economia.csv"
)
wdi_df[["name", "region_id", "year"] + list(set(wdi_df.columns.str.lower().to_list()) & set(etl.salud))].to_csv(
    "../datasets/sql/world_development_indicators/wdi_salud.csv"
)
wdi_df[["name", "region_id", "year"] + list(set(wdi_df.columns.str.lower().to_list()) & set(etl.educacion))].to_csv(
    "../datasets/sql/world_development_indicators/wdi_educacion.csv"
)
wdi_df[["name", "region_id", "year"] + list(set(wdi_df.columns.str.lower().to_list()) & set(etl.empleos))].to_csv(
    "../datasets/sql/world_development_indicators/wdi_empleos.csv"
)
wdi_df[["name", "region_id", "year"] + list(set(wdi_df.columns.str.lower().to_list()) & set(etl.poblacion))].to_csv(
    "../datasets/sql/world_development_indicators/wdi_poblacion.csv"
)
