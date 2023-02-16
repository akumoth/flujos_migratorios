import pycountry
import pandas as pd
import pycountry
import numpy as np
import re
from geopy.geocoders import Nominatim
import geonamescache

from peewee import chunked
from peewee_models import *

country_code_df = pd.read_csv('../datasets/processed/codigo_pais.csv')
country_code_df.columns = ['region','region_id']
country_code_df.set_index('region',inplace=True)

geolocator = Nominatim(user_agent="geoapiExercises")

def normalize_country(name):
    custom_mapping = {
        "iran, islamic republic of": "iran",
        "viet nam" : "vietnam",
        "taiwan, province of china" : "taiwan",
        "vie tnam": "vietnam",
        "spain*": "spain",
        "Iran (Islamic Republic of)": "iran",
        "côte d'ivoire": "cote d'ivoire",
        "China, Hong Kong SAR*": "hong kong",
        "hong kong sar, china": "hong kong",
        "iran, islamic rep.": "iran",
        "turkiye": "turkey",
        "United States of America*": "United States",
        "Iran (Islamic Republic of)": "iran",
        "Russian Federation": "russia",
        "France*": "France",
        "Australia*": "Australia",
        "United Kingdom*": "United Kingdom",
        "China, Hong Kong SAR*": "hong kong", 
        "Ukraine*": "Ukraine",
        "iran islamic republic of": "iran",
        "curazao" : "curacao",
        "saint barthlemy" : "saint barth",
        "bolivia plurinational state of": "bolivia",
        "democratic republic of the congo" : "congo",
        "guineabisau" : "guinea-bissau",
        "guinea-bisau" : "guinea-bissau",
        "guineabissau" : "guinea-bissau",
        "china hong kong sar": "hong kong",
        "china macao sar": "macao",
        "china taiwan province of china": "taiwan",
        "dem peoples republic of korea": "north korea",
        "palestina" : "palestine",
        "palestine, state of": "palestine",
        "russian federation": "russia",
        "bolivia, plurinational state of": "bolivia",
        "maldovia": "republic of maldova",
        "moldova, republic of": "republic of maldova",
        "siria": "syrian",
        "syrian arab republic": "syrian"

    }
    
    if name in custom_mapping:
        return custom_mapping[name]
    
    # Buscar el país más cercano al nombre normalizado
    try: 
        # country = pycountry.countries.search_fuzzy(name) - Añadir después
        country = pycountry.countries.lookup(name)
        print(country)
        return country.name
    except LookupError:
        return name

def remove_special_characters(text):
    return re.sub(r"[^a-zA-Z0-9\s]+", "", text)

def get_lat_long(country_name):
    location = geolocator.geocode(country_name)
    if location is not None:
        return (location.latitude, location.longitude)
    else:
        location.latitude, location.longitude = np.NaN
        return location.latitude, location.longitude

def insert_country_code(df):
    df.insert((df.columns.get_loc("region")+1),'region_id',df.join(country_code_df,on='region',how='left',validate='m:1')['region_id'])
    df.dropna(inplace=True)
    df['region_id'] = df['region_id'].astype(int)

def insert_lat_long(df):
    lat = []
    log = []
    for item in df['region']:
        direction = geolocator.geocode(item, timeout=10)
        if direction is None:
            latitude = None
            longitude = None
        else:
            latitude = direction.latitude
            longitude = direction.longitude
        lat.append(latitude)
        log.append(longitude)
    df['latitude'] = pd.Series(lat)
    df['longitude'] = pd.Series(log)

def insert_data(df):
    with database.atomic():
        for batch in chunked(df[["region_id", "year"] + list(set(df.columns.str.lower().to_list()) & set(poblacion))].to_dict(orient="records"), 100):
            Demography.insert_many(batch).on_conflict_replace(True).execute()
        for batch in chunked(df[["region_id", "year"] + list(set(df.columns.str.lower().to_list()) & set(economia))].to_dict(orient="records"), 100):
            Economy.insert_many(batch).on_conflict_replace(True).execute()
        for batch in chunked(df[["region_id", "year"] + list(set(df.columns.str.lower().to_list()) & set(educacion))].to_dict(orient="records"), 100):
            Education.insert_many(batch).on_conflict_replace(True).execute()
        for batch in chunked(df[["region_id", "year"] + list(set(df.columns.str.lower().to_list()) & set(empleos))].to_dict(orient="records"), 100):
            Employment.insert_many(batch).on_conflict_replace(True).execute()
        for batch in chunked(df[["region_id", "year"] + list(set(df.columns.str.lower().to_list()) & set(salud))].to_dict(orient="records"), 100):
            Health.insert_many(batch).on_conflict_replace(True).execute()

def obtener_idioma_principal(pais):
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    for codigo, detalles in countries.items():
        if str.lower(detalles['name']) == pais:
            idioma_principal = detalles['languages'].split(',')[0]
            return idioma_principal
    return None
# Características a contemplar para nuestro ETL

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
    "intentional homicides (per 100,000 people)",
    "death rate, crude (per 1,000 people)",
    'male life expectancy at birth (years)',
    'female life expectancy at birth (years)',
    'male deaths (thousands)',
    'female deaths (thousands)',
    'births (thousands)',
    'total fertility rate (live births per woman)',
    'net reproduction rate (surviving daughters per woman)',
    'male mortality between age 15 and 50 (deaths under age 50 per 1,000 males alive at age 15)',
    'female mortality between age 15 and 50 (deaths under age 50 per 1,000 females alive at age 15)',
    'infant deaths, under age 1 (thousands)',
    'under-five deaths, under age 5 (thousands)',
    'infant mortality rate (infant deaths per 1,000 live births)',
    'mean age childbearing (years)',
    "domestic private health expenditure per capita (current us$)",
    "domestic general government health expenditure per capita (current us$)",
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
    "male population, as of 1 july (thousands)",
    'female population, as of 1 july (thousands)',
    'median age, as of 1 july (years)',
    "individuals using the internet (% of population)",
    "international migrant stock, total",
    "international migrant stock (% of population)",
    'net number of migrants (thousands)',
    'net migration rate (per 1,000 population)',
    "population ages 0-14 (% of total population)",
    "population density (people per sq. km of land area)",
    "population growth (annual %)",
    "population in largest city",
    "population in the largest city (% of urban population)",
    "refugee population by country or territory of asylum",
    "refugee population by country or territory of origin",
    "rural population (% of total population)",
    "rural population growth (annual %)",
    "urban population (% of total population)",
    "urban population growth (annual %)",
    "multidimensional poverty headcount ratio (% of total population)",
]

economia = [i.replace("%", "percent") for i in economia]
economia = [remove_special_characters(i) for i in economia]
economia = [i.replace(" ", "_") for i in economia]

salud = [i.replace("%", "percent") for i in salud]
salud = [remove_special_characters(i) for i in salud]
salud = [i.replace(" ", "_") for i in salud]

educacion = [i.replace("%", "percent") for i in educacion]
educacion = [remove_special_characters(i) for i in educacion]
educacion = [i.replace(" ", "_") for i in educacion]

empleos = [i.replace("%", "percent") for i in empleos]
empleos = [remove_special_characters(i) for i in empleos]
empleos = [i.replace(" ", "_") for i in empleos]

poblacion = [i.replace("%", "percent") for i in poblacion]
poblacion = [remove_special_characters(i) for i in poblacion]
poblacion = [i.replace(" ", "_") for i in poblacion]
