import pandas as pd
import normalization
from peewee import chunked
from peewee_models import *

country_code_df = pd.read_csv("../datasets/processed/codigo_pais.csv")
wdi_df = pd.read_csv(
    "../datasets/processed/world_development_indicators/world_development_indicators.csv"
)

# Definición de las categorias en las que dividiremos este dataset antés de cargarlo

economia = [
    "adjusted net national income (current us$)",
    "adjusted net national income per capita (annual % growth)",
    "adjusted savings: gross savings (% of gni)",
    "cost of business start-up procedures (% of gni per capita)",
    "cost of business start-up procedures, female (% of gni per capita)",
    "cost of business start-up procedures, male (% of gni per capita)",
    "domestic credit to private sector by banks (% of gdp)",
    "domestic credit to private sector (% of gdp)",
    "ease of doing business score (0 = lowest performance to 100 = best performance)",
    "foreign direct investment, net (bop, current us$)",
    "gdp (current us$)",
    "gdp growth (annual %)",
    "gini index",
    "gni (current us$)",
    "gni growth (annual %)",
    "gross domestic savings (current us$)",
    "gross domestic savings (% of gdp)",
    "gross savings (% of gdp)",
    "gross savings (% of gni)",
    "industry (including construction), value added (% of gdp)",
    "industry (including construction), value added (annual % growth)",
    "inflation, consumer prices (annual %)",
    "investment in ict with private participation (current us$)",
    "labor force, total",
    "labor tax and contributions (% of commercial profits)",
    "listed domestic companies, total",
    "market capitalization of listed domestic companies (current us$)",
    "market capitalization of listed domestic companies (% of gdp)",
    "multidimensional poverty headcount ratio (% of total population)",
    "net trade in goods and services (bop, current us$)",
    "new business density (new registrations per 1,000 people ages 15-64)",
    "new businesses registered (number)",
    "personal remittances, received (current us$)",
    "personal remittances, received (% of gdp)",
    "personal remittances, paid (current us$)",
    "profit tax (% of commercial profits)",
    "research and development expenditure (% of gdp)",
    "researchers in r&d (per million people)",
    "tax payments (number)",
    "tax revenue (% of gdp)",
    "taxes on income, profits and capital gains (% of total taxes)",
    "time spent dealing with the requirements of government regulations (% of senior management time)",
    "unemployment, total (% of total labor force) (national estimate)",
    "unemployment, total (% of total labor force) (modeled ilo estimate)",
]

salud = [
    "cause of death, by communicable diseases and maternal, prenatal and nutrition conditions (% of total)",
    "cause of death, by non-communicable diseases (% of total)",
    "death rate, crude (per 1,000 people)",
    "domestic private health expenditure per capita (current us$)",
    "domestic general government health expenditure per capita (current us$)",
    "intentional homicides (per 100,000 people)",
    "life expectancy at birth, total (years)",
    "people using at least basic drinking water services (% of population)",
    "people with basic handwashing facilities including soap and water (% of population)",
    "pregnant women receiving prenatal care (%)",
    "prevalence of moderate or severe food insecurity in the population (%)",
    "suicide mortality rate (per 100,000 population)",
]

educacion = [
    "educational attainment, at least bachelor's or equivalent, population 25+, total (%) (cumulative)",
    "educational attainment, at least completed lower secondary, population 25+, total (%) (cumulative)",
    "educational attainment, at least completed upper secondary, population 25+, total (%) (cumulative)",
    "educational attainment, at least master's or equivalent, population 25+, total (%) (cumulative)",
    "educational attainment, doctoral or equivalent, population 25+, total (%) (cumulative)",
    "technicians in r&d (per million people)",
]

empleos = [
    "employers, total (% of total employment) (modeled ilo estimate)",
    "employment in agriculture (% of total employment) (modeled ilo estimate)",
    "employment in industry (% of total employment) (modeled ilo estimate)",
    "employment in services (% of total employment) (modeled ilo estimate)",
    "firms offering formal training (% of firms)",
    "self-employed, total (% of total employment) (modeled ilo estimate)",
    "time required to start a business (days)",
    "time required to register property (days)",
    "time required to start a business, female (days)",
    "time required to start a business, male (days)",
    "labor force, total",
    "unemployment, total (% of total labor force) (national estimate)",
    "unemployment, total (% of total labor force) (modeled ilo estimate)",
]

poblacion = [
    "individuals using the internet (% of population)",
    "international migrant stock, total",
    "international migrant stock (% of population)",
    "net migration",
    "population ages 0-14 (% of total population)",
    "population density (people per sq. km of land area)",
    "population growth (annual %)",
    "population in largest city",
    "population in the largest city (% of urban population)",
    "population, total",
    "refugee population by country or territory of asylum",
    "refugee population by country or territory of origin",
    "rural population (% of total population)",
    "rural population growth (annual %)",
    "urban population (% of total population)",
    "urban population",
    "urban population growth (annual %)",
    "multidimensional poverty headcount ratio (% of total population)",
]

economia = [i.replace("%", "percent") for i in economia]
economia = [normalization.remove_special_characters(i) for i in economia]
economia = [i.replace(" ", "_") for i in economia]

salud = [i.replace("%", "percent") for i in salud]
salud = [normalization.remove_special_characters(i) for i in salud]
salud = [i.replace(" ", "_") for i in salud]

educacion = [i.replace("%", "percent") for i in educacion]
educacion = [normalization.remove_special_characters(i) for i in educacion]
educacion = [i.replace(" ", "_") for i in educacion]

empleos = [i.replace("%", "percent") for i in empleos]
empleos = [normalization.remove_special_characters(i) for i in empleos]
empleos = [i.replace(" ", "_") for i in empleos]

poblacion = [i.replace("%", "percent") for i in poblacion]
poblacion = [normalization.remove_special_characters(i) for i in poblacion]
poblacion = [i.replace(" ", "_") for i in poblacion]

# Renombramos y limpiamos columnas en el dataframe de WDI

wdi_df = wdi_df.rename(
    {"Country Name": "region", "Series Name": "conditions"}, axis=1
).drop(["Unnamed: 0", "Country Code"], axis=1)

j = []
for i in wdi_df.columns:
    j.append(i.split(" ")[0])
wdi_df.columns = j

# Renombramos los valores de Series Name en el dataframe de WDI

wdi_df["conditions"] = wdi_df["conditions"].str.replace("%", "percent")
wdi_df["conditions"] = wdi_df["conditions"].apply(
    normalization.remove_special_characters
)
wdi_df["conditions"] = wdi_df["conditions"].str.replace(" ", "_")

# Transponemos el dataframe de WDI de manera tal que queden los años como filas y las condiciones como columnas

wdi_df = (
    wdi_df.set_index(["region", "conditions"])
    .rename_axis("year", axis=1)
    .stack()
    .unstack(1)
    .reset_index()
    .rename_axis(None, axis=1)
    .rename_axis("id")
)

normalization.insert_country_code(wdi_df)
wdi_df[["region", "region_id", "year"] + economia].to_csv(
    "../datasets/sql/world_development_indicators/wdi_economia.csv"
)
wdi_df[["region", "region_id", "year"] + salud].to_csv(
    "../datasets/sql/world_development_indicators/wdi_salud.csv"
)
wdi_df[["region", "region_id", "year"] + educacion].to_csv(
    "../datasets/sql/world_development_indicators/wdi_educacion.csv"
)
wdi_df[["region", "region_id", "year"] + empleos].to_csv(
    "../datasets/sql/world_development_indicators/wdi_empleos.csv"
)
wdi_df[["region", "region_id", "year"] + poblacion].to_csv(
    "../datasets/sql/world_development_indicators/wdi_poblacion.csv"
)

with database.atomic():
    for batch in chunked(wdi_df[["region", "region_id", "year"] + poblacion].to_dict(orient="records"),100):
        Demography.insert_many(batch).execute()
    for batch in chunked(wdi_df[["region", "region_id", "year"] + economia].to_dict(orient="records"),100):
        Economy.insert_many(batch).execute()
    for batch in chunked(wdi_df[["region", "region_id", "year"] + educacion].to_dict(orient="records"),100):
        Education.insert_many(batch).execute()
    for batch in chunked(wdi_df[["region", "region_id", "year"] + empleos].to_dict(orient="records"),100):
        Employment.insert_many(batch).execute()
    for batch in chunked(wdi_df[["region", "region_id", "year"] + salud].to_dict(orient="records"),100):
        Health.insert_many(batch).execute()
