import pandas as pd
import etl

wdi_df = pd.read_csv(
    "../datasets/processed/world_development_indicators/P-world_development_indicators.csv"
).drop('region_id',axis=1)

# Renombramos y limpiamos columnas en el dataframe de WDI

wdi_df = wdi_df.rename(
    {"Country name": "name", "Series Name": "conditions"}, axis=1
)

j = []
for i in wdi_df.columns:
    j.append(i.split(" ")[0])
wdi_df.columns = j

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

wdi_columns = wdi_df.columns.to_series()
wdi_columns = wdi_columns.str.lower()
wdi_columns = etl.normalize_lists(wdi_columns)
wdi_df.columns = wdi_columns

# Normalizamos los nombres de los países 

wdi_df['name'] = wdi_df['name'].apply(etl.normalize_country).str.lower()
etl.insert_country_code(wdi_df)

# Borramos los países que no esten en nuestra lista de valores a contemplar 

wdi_df.drop(wdi_df.where(~wdi_df.name.isin(etl.country_code_df['name'])).dropna().index,axis=0)


print(wdi_df.columns[wdi_df.columns.str.contains('internet')])

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
