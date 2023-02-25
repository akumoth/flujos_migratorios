import pandas as pd
import etl

# Importación de datos

wpp_df = pd.read_excel("../datasets/raw/world_population_prospects/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx", index_col=0)
wpp_df.drop(['Variant','Notes','Location code','ISO3 Alpha-code','ISO2 Alpha-code','SDMX code**','Parent code'],axis=1,inplace=True)

# Normalización de columnas

wpp_columns = wpp_df.columns.to_series()
wpp_columns[0] = 'name'
wpp_columns = wpp_columns.str.lower()
wpp_columns = etl.normalize_lists(wpp_columns)
wpp_df.columns = wpp_columns
wpp_df.name = wpp_df.name.astype(str)
wpp_df.type = wpp_df.type.astype(str)

# Conversión de campos numericos al tipo de dato Float

for i in wpp_df.columns[2:]:
    wpp_df[i] = wpp_df[i].replace('...',None)
    wpp_df[i] = pd.to_numeric(wpp_df[i],downcast='float')
    
# División en dos DF (uno de regiones, y otro según grupos de desarrollo)

reg_wpp_df = wpp_df[(wpp_df.type != 'World') & (wpp_df.type != 'Label/Separator') & (wpp_df.type != 'Development Group') & (wpp_df.type != 'Income Group') & (wpp_df.type != 'Special other')]
dev_wpp_df = wpp_df[(wpp_df.type == 'Development Group') | (wpp_df.type == 'Income Group') | (wpp_df.type == 'Special other')]


# Inserción del codigo país

reg_wpp_df['name'] = reg_wpp_df['name'].apply(etl.normalize_country).str.lower()
etl.insert_country_code(reg_wpp_df)

# Conversión de los DF a CSVs 

reg_wpp_df.to_csv('../datasets/processed/world_population_prospects/WPP_by_region.csv')
dev_wpp_df.to_csv('../datasets/processed/world_population_prospects/WPP_by_development.csv')

# Borramos los países que no esten en nuestra lista de valores a contemplar 

reg_wpp_df = reg_wpp_df.drop('type',axis=1)
reg_wpp_df = reg_wpp_df.drop(reg_wpp_df.where(~reg_wpp_df.name.isin(etl.country_code_df['name'])).dropna().index,axis=0)

# Renombrando el indice a "id"

reg_wpp_df = reg_wpp_df.drop(reg_wpp_df.where((reg_wpp_df.year < 1990) | (reg_wpp_df.year > 2020)).dropna().index,axis=0).sort_values(['name','year']).reset_index(drop=True).rename_axis("id")
reg_wpp_df.year = reg_wpp_df.year.astype(int)

# Generamos los archivos CSV, dividiendo la información según las tablas planteadas para la base de datos.

reg_wpp_df[["name", "region_id", "year"] + list(set(reg_wpp_df.columns.str.lower().to_list()) & set(etl.salud))].to_csv(
    "../datasets/sql/world_population_prospects/wpp_salud.csv"
)
reg_wpp_df[["name", "region_id", "year"] + list(set(reg_wpp_df.columns.str.lower().to_list()) & set(etl.poblacion))].to_csv(
    "../datasets/sql/world_population_prospects/wpp_poblacion.csv"
)
