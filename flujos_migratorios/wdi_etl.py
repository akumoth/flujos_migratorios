import pandas as pd
import numpy as np
import etl

# Carga inicial de los conjuntos de datos.
# Al realizar su normalización inicial, se detallaron ciertas columnas que serían inutiles para nuestra base de datos, 
# las cuales quitamos al cargar.

wdi_df = pd.read_csv(
    "../datasets/processed/world_development_indicators/P-world_development_indicators.csv"
).drop('region_id',axis=1)

wdi_salud_indicador_df = pd.read_csv(
    "../datasets/processed/world_development_indicators/indicador_de_salud_normalizado.csv"
).drop('Unnamed: 0', axis=1)

wdi_educacion_indicador_df = pd.read_csv(
    "../datasets/processed/world_development_indicators/indicador_educacion_normalizado.csv"
).drop('Unnamed: 0', axis=1)

# Estandarización de columnas:

def pre_normalization(df):
    for i in df.columns.to_list():
        # Cambiando todas las columnas de tipo cadena a minusculas
        if pd.api.types.is_string_dtype(df[i]):
            df[i] = df[i].str.lower()
        # y, en caso de que sean dos palabras, utilizando nada más la primera
        df = df.rename({i:str(i).split(" ")[0]},axis=1)
    # Además, se estandarizaran los nombres a lo largo de los distintos conjuntos de datos
    df.rename({"Country":"name","Series":"conditions"},axis=1,inplace=True)
    return df

# La función definida anteriormente la utilizamos para normalizar los dataframes.
wdi_df = pre_normalization(wdi_df)
wdi_salud_indicador_df = pre_normalization(wdi_salud_indicador_df)
wdi_educacion_indicador_df = pre_normalization(wdi_educacion_indicador_df)

# Concatenamos los anteriores df en uno solo.
wdi_df = pd.concat([wdi_df,wdi_educacion_indicador_df,wdi_salud_indicador_df]).replace([np.nan], [None]).replace([0.0], [None])
wdi_df = wdi_df.reset_index(drop=True)

# Pivoteo para que quedé del mismo formato que la tabla SQL, volviendo el año una columna
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

# Normalizamos los nombres de los indicadores en "conditions" con la función anteriormente definida en el modulo etl
wdi_df.columns = etl.normalize_lists(wdi_df.columns.str.lower())

# Normalizamos los nombres de los países 
wdi_df['name'] = wdi_df['name'].apply(etl.normalize_country).str.lower()
etl.insert_country_code(wdi_df)

# Borramos los países que no estén en nuestro modelo, y estandarizamos los valores faltantes como "None" 

wdi_df = wdi_df.drop(wdi_df.where(~wdi_df.name.isin(etl.country_code_df['name'])).dropna().index,axis=0)
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
