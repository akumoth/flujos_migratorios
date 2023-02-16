import pandas as pd
import numpy as np
import etl
from peewee import chunked
from peewee_models import *

# Importación de datos

wpp_df = pd.read_excel("../datasets/raw/world_population_prospects/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx", index_col=0)
wpp_df.drop(['Variant','Notes','Location code','ISO3 Alpha-code','ISO2 Alpha-code','SDMX code**','Parent code'],axis=1,inplace=True)
country_code_df = pd.read_csv('../datasets/processed/codigo_pais.csv')

# Normalización de columnas

wpp_columns = wpp_df.columns.to_series()
wpp_columns[0] = 'region'
wpp_columns = wpp_columns.str.lower()
wpp_columns = [i.replace("%", "percent") for i in wpp_columns]
wpp_columns = [etl.remove_special_characters(i) for i in wpp_columns]
wpp_columns = [i.replace(" ", "_") for i in wpp_columns]
wpp_df.columns = wpp_columns
wpp_df.region = wpp_df.region.astype(str)
wpp_df.type = wpp_df.type.astype(str)

# División en dos DF (uno de regiones, y otro según grupos de desarrollo)

reg_wpp_df = wpp_df[(wpp_df.type != 'World') & (wpp_df.type != 'Label/Separator') & (wpp_df.type != 'Development Group') & (wpp_df.type != 'Income Group') & (wpp_df.type != 'Special other')]
dev_wpp_df = wpp_df[(wpp_df.type == 'Development Group') | (wpp_df.type == 'Income Group') | (wpp_df.type == 'Special other')]

# Conversión de campos numericos al tipo de dato Float

for i in reg_wpp_df.columns[2:]:
    reg_wpp_df[i] = reg_wpp_df[i].astype(str).str.replace('...','0',regex=False)
    reg_wpp_df[i] = pd.to_numeric(reg_wpp_df[i],downcast='float')

for i in dev_wpp_df.columns[2:]:
    dev_wpp_df[i] = dev_wpp_df[i].astype(str).str.replace('...','0',regex=False)
    dev_wpp_df[i] = pd.to_numeric(dev_wpp_df[i],downcast='float')

# Inserción del codigo país

reg_wpp_df['region'] = reg_wpp_df['region'].apply(etl.normalize_country).str.lower()
etl.insert_country_code(reg_wpp_df)

# Conversión de los DF a CSVs 

reg_wpp_df.to_csv('../datasets/processed/world_population_prospects/WPP_by_region.csv')
dev_wpp_df.to_csv('../datasets/processed/world_population_prospects/WPP_by_development.csv')

### Carga de los datos a nuestra base de datos

