import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# Importación de datos

wpp_df = pd.read_excel("../datasets/raw/world_population_prospects/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx", index_col=0)
wpp_df.drop(['Variant','Notes','Location code','ISO3 Alpha-code','ISO2 Alpha-code','SDMX code**','Parent code'],axis=1,inplace=True)

# Normalización de columnas

wpp_columns = wpp_df.columns.to_series()
wpp_columns[0] = 'Region'
wpp_columns = wpp_columns.str.lower()
wpp_columns = wpp_columns.str.replace(',','')
wpp_columns = wpp_columns.str.replace(' ','_')
wpp_columns = wpp_columns.str.replace('(','_',regex=False)
wpp_columns = wpp_columns.str.replace(')','_',regex=False)
wpp_df.columns = wpp_columns
wpp_df.region = wpp_df.region.astype(str)
wpp_df.type = wpp_df.type.astype(str)

# División en dos DF (uno de regiones, y otro según grupos de desarrollo) y conversión de tipos de datos

reg_wpp_df = wpp_df[(wpp_df.type != 'World') & (wpp_df.type != 'Label/Separator') & (wpp_df.type != 'Development Group') & (wpp_df.type != 'Income Group') & (wpp_df.type != 'Special other')]
dev_wpp_df = wpp_df[(wpp_df.type == 'Development Group') | (wpp_df.type == 'Income Group') | (wpp_df.type == 'Special other')]

for i in reg_wpp_df.columns[2:]:
    reg_wpp_df[i] = reg_wpp_df[i].astype(str).str.replace('...','0',regex=False)
    reg_wpp_df[i] = pd.to_numeric(reg_wpp_df[i],downcast='float')

for i in dev_wpp_df.columns[2:]:
    dev_wpp_df[i] = reg_wpp_df[i].astype(str).str.replace('...','0',regex=False)
    dev_wpp_df[i] = pd.to_numeric(reg_wpp_df[i],downcast='float')

reg_wpp_df.to_csv('../datasets/processed/world_population_prospects/WPP_by_region.csv')
dev_wpp_df.to_csv('../datasets/processed/world_population_prospects/WPP_by_development.csv')