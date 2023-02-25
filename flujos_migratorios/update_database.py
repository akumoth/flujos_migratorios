import pandas as pd
import numpy as np
from peewee_models import *
import os

os.system('wdi_etl.py')
os.system('wpp_etl.py')
os.system('pvp_etl.py')

# Transformación y concatenación de los csv anteriormente generados a un solo dataframe para ingestarlos después a la base de datos

wpp_poblacion = pd.read_csv("../datasets/sql/world_population_prospects/wpp_poblacion.csv")
wdi_poblacion = pd.read_csv("../datasets/sql/world_development_indicators/wdi_poblacion.csv")
wpp_poblacion.set_index(["region_id", "year"], inplace=True)
wdi_poblacion.set_index(["region_id", "year"], inplace=True)
table_poblacion = wpp_poblacion.merge(wdi_poblacion, how="right", left_index=True, right_index=True).drop(['id_x','name_x','id_y','name_y'],axis=1).reset_index()
table_poblacion = table_poblacion[table_poblacion['region_id'].notna()]
table_poblacion = table_poblacion.replace(np.nan, None).reset_index(drop=True)
table_poblacion.region_id = table_poblacion.region_id.astype(int)
table_poblacion.insert(1,'region_id',table_poblacion.pop('region_id'))

wpp_salud = pd.read_csv("../datasets/sql/world_population_prospects/wpp_salud.csv")
wdi_salud = pd.read_csv("../datasets/sql/world_development_indicators/wdi_salud.csv")
wpp_salud.set_index(["region_id", "year"], inplace=True)
wdi_salud.set_index(["region_id", "year"], inplace=True)
table_salud = wpp_salud.merge(wdi_salud, how="right", left_index=True, right_index=True).drop(['id_x','name_x','id_y','name_y'],axis=1).reset_index()
table_salud = table_salud[table_salud['region_id'].notna()]
table_salud = table_salud.replace(np.nan, None).reset_index(drop=True)
table_salud.region_id = table_salud.region_id.astype(int)
table_salud.insert(1,'region_id',table_salud.pop('region_id'))

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