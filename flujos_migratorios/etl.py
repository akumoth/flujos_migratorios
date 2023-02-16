import pycountry
import pandas as pd
import numpy as np
import re
from geopy.geocoders import Nominatim

country_code_df = pd.read_csv('../datasets/processed/codigo_pais.csv')
country_code_df.columns = ['region','region_id']
country_code_df.set_index('region',inplace=True)

geolocator = Nominatim(user_agent="geoapiExercises")

def normalize_country(name):
    custom_mapping = {
        "Iran (Islamic Republic of)": "iran",
        "côte d'ivoire": "cote d'ivoire",
        "China, Hong Kong SAR*": "hong kong",
        "hong kong sar, china": "hong kong",
        "iran, islamic rep.": "iran"
    }
    
    if name in custom_mapping:
        return custom_mapping[name]
    try:
        country = pycountry.countries.lookup(name)
        return country.name
    except LookupError:
        if name == "United States of America*":
            return "United States"
        elif name == "Iran (Islamic Republic of)":
            return "Iran"
        elif name == "Russian Federation":
            return "Russia"
        elif name == "France*":
            return "France"
        elif name == "Australia*":
            return "Australia"
        elif name == "United Kingdom*":
            return "United Kingdom"
        elif name == "China, Hong Kong SAR*":
            return "Hong Kong"                 
        elif name == "Ukraine*":
            return "Ukraine"
        # agrega más verificaciones aquí para otros casos especiales
        else:
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
