import pandas as pd
import numpy as np
from peewee_models import *
import os

os.system('wdi_etl.py')
os.system('wpp_etl.py')
os.system('pvp_etl.py')

# Transformación y concatenación de los csv anteriormente generados a un solo dataframe para ingestarlos después a la base de datos

def merge_migration_datasets(df1,df2):
    df = df1.merge(df2, how="right", left_index=True, right_index=True).drop(['id_x','name_x','id_y','name_y'],axis=1).reset_index()
    df = df[df['region_id'].notna()]
    df = df.replace(np.nan, None).reset_index(drop=True)
    df.region_id = df.region_id.astype(int)
    df.insert(1,'region_id',df.pop('region_id'))
    return df

wpp_poblacion = pd.read_csv("../datasets/sql/world_population_prospects/wpp_poblacion.csv").set_index(["region_id", "year"])
wdi_poblacion = pd.read_csv("../datasets/sql/world_development_indicators/wdi_poblacion.csv").set_index(["region_id", "year"])
table_poblacion = merge_migration_datasets(wpp_poblacion,wdi_poblacion)

wpp_salud = pd.read_csv("../datasets/sql/world_population_prospects/wpp_salud.csv").set_index(["region_id", "year"])
wdi_salud = pd.read_csv("../datasets/sql/world_development_indicators/wdi_salud.csv").set_index(["region_id", "year"])
table_salud = merge_migration_datasets(wpp_salud,wdi_salud)

wdi_economia = pd.read_csv("../datasets/sql/world_development_indicators/wdi_economia.csv").drop(['id','name'],axis=1)
table_economia = wdi_economia
table_economia = table_economia.replace(np.nan, None)

wdi_educacion = pd.read_csv("../datasets/sql/world_development_indicators/wdi_educacion.csv").drop(['id','name'],axis=1)
table_educacion = wdi_educacion
table_educacion = table_educacion.replace(np.nan, None)

wdi_empleos = pd.read_csv("../datasets/sql/world_development_indicators/wdi_empleos.csv").drop(['id','name'],axis=1)
table_empleos = wdi_empleos
table_empleos = table_empleos.replace(np.nan, None)

migration = pd.read_csv("../datasets/sql/migration.csv")
table_migration = migration
table_migration = table_migration.replace(np.nan, None)

# Ingesta de datos en los dataframes relevantes

with database.atomic():
    for batch in chunked(table_poblacion.to_dict(orient="records"), 100):
        Demography.insert_many(batch).on_conflict_replace(True).execute()
    for batch in chunked(table_economia.to_dict(orient="records"), 100):
        Economy.insert_many(batch).on_conflict_replace(True).execute()
    for batch in chunked(table_educacion.to_dict(orient="records"), 100):
        Education.insert_many(batch).on_conflict_replace(True).execute()
    for batch in chunked(table_empleos.to_dict(orient="records"), 100):
        Employment.insert_many(batch).on_conflict_replace(True).execute()
    for batch in chunked(table_salud.to_dict(orient="records"), 100):
        Health.insert_many(batch).on_conflict_replace(True).execute()
    for batch in chunked(table_migration.to_dict(orient="records"), 100):
        Migration.insert_many(batch).on_conflict_replace(True).execute()