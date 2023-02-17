import pandas as pd
from peewee_models import *

wpp_poblacion = pd.read_csv("../datasets/sql/world_population_prospects/wpp_poblacion.csv")
wdi_poblacion = pd.read_csv("../datasets/sql/world_development_indicators/wdi_poblacion.csv")
wpp_poblacion.set_index(["region_id", "year"], inplace=True)
wdi_poblacion.set_index(["region_id", "year"], inplace=True)
table_poblacion = wpp_poblacion.merge(wdi_poblacion, how="right", left_index=True, right_index=True).drop(['id_x','name_x','id_y','name_y'],axis=1).reset_index()

wpp_salud = pd.read_csv("../datasets/sql/world_population_prospects/wpp_salud.csv")
wdi_salud = pd.read_csv("../datasets/sql/world_development_indicators/wdi_salud.csv")
wpp_salud.set_index(["region_id", "year"], inplace=True)
wdi_salud.set_index(["region_id", "year"], inplace=True)
table_salud = wpp_salud.merge(wdi_salud, how="right", left_index=True, right_index=True).drop(['id_x','name_x','id_y','name_y'],axis=1).reset_index()

wdi_economia = pd.read_csv("../datasets/sql/world_development_indicators/wdi_economia.csv").drop(['id','name'],axis=1)
table_economia = wdi_economia

wdi_educacion = pd.read_csv("../datasets/sql/world_development_indicators/wdi_educacion.csv").drop(['id','name'],axis=1)
table_educacion = wdi_educacion

wdi_empleos = pd.read_csv("../datasets/sql/world_development_indicators/wdi_empleos.csv").drop(['id','name'],axis=1)
table_empleos = wdi_empleos

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
