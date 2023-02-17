import pandas as pd
import etl

wdi_df = pd.read_csv(
    "../datasets/processed/world_development_indicators/world_development_indicators.csv"
)

# Renombramos y limpiamos columnas en el dataframe de WDI

wdi_df = wdi_df.rename(
    {"Country Name": "name", "Series Name": "conditions"}, axis=1
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
    wdi_df.set_index(["name", "conditions"])
    .rename_axis("year", axis=1)
    .stack()
    .unstack(1)
    .sort_values(['name','year'])
    .reset_index()
    .rename_axis(None, axis=1)
    .rename_axis("id")
)

# Normalizamos los nombres de los países 

wdi_df['name'] = wdi_df['name'].apply(etl.normalize_country).str.lower()
etl.insert_country_code(wdi_df)

# Borramos los países que no esten en nuestra lista de valores a contemplar 

wdi_df.drop(wdi_df.where(~wdi_df.name.isin(etl.country_code_df['name'])).dropna().index,axis=0)

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
