import pycountry
import pandas as pd
import pycountry
import numpy as np
import re
from geopy.geocoders import Nominatim
import geonamescache

country_code_df = pd.read_csv('../datasets/processed/codigo_pais.csv').drop('Unnamed: 0',axis=1)
country_code_df['cod'] = country_code_df['cod'].astype(int)
country_code_df.columns = ['name','lang','cod','lat','long']
country_code_df = country_code_df.sort_values('cod').reset_index(drop=True)
country_code_df.index = np.arange(1, len(country_code_df) + 1)
country_code_df = country_code_df.drop('cod',axis=1).reset_index(names='cod')

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
    for name in df['name'].unique():
        subset = df[df['name'] == name]
        codes = country_code_df[country_code_df['name'] == name]['cod']
        code_str = ', '.join(codes.astype(str))
        df.loc[df['name'] == name, 'region_id'] = code_str

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
    df.insert(df.shape[1],'latitude',pd.Series(lat))
    df.insert(df.shape[1],'longitude',pd.Series(log))

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
    "cost of business start-up procedures, female (% of gni per capita)",
    "cost of business start-up procedures, male (% of gni per capita)",
    "domestic credit to private sector (% of gdp)",
    "ease of doing business score (0 = lowest performance to 100 = best performance)",
    "foreign direct investment, net (bop, current us$)",
    "gdp (current us$)",
    "gini index",
    "gni (current us$)",
    "gross domestic savings (current us$)",
    "gross savings (% of gdp)",
    "gross savings (% of gni)",
    "industry (including construction), value added (% of gdp)",
    "inflation, consumer prices (annual %)",
    "investment in ict with private participation (current us$)",
    "labor force, total",
    "labor tax and contributions (% of commercial profits)",
    "listed domestic companies, total",
    "market capitalization of listed domestic companies (current us$)",
    "multidimensional poverty headcount ratio (% of total population)",
    "net trade in goods and services (bop, current us$)",
    "new businesses registered (number)",
    "personal remittances, received (current us$)",
    "personal remittances, paid (current us$)",
    "profit tax (% of commercial profits)",
    "research and development expenditure (% of gdp)",
    "researchers in r&d (per million people)",
    "tax payments (number)",
    "tax revenue (% of gdp)",
    "taxes on income, profits and capital gains (% of total taxes)",
    "time spent dealing with the requirements of government regulations (% of senior management time)",
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
    "self-employed, total (% of total employment) (modeled ilo estimate)",
    "time required to register property (days)",
    "time required to start a business, female (days)",
    "time required to start a business, male (days)",
    "labor force, total",
    "unemployment, total (% of total labor force) (national estimate)",
]

poblacion = [
    "male population, as of 1 july (thousands)",
    'female population, as of 1 july (thousands)',
    'median age, as of 1 july (years)',
    "individuals using the internet (% of population)",
    "international migrant stock, total",
    'net number of migrants (thousands)',
    'net migration rate (per 1,000 population)',
    "population ages 0-14 (% of total population)",
    "population density (people per sq. km of land area)",
    "population growth (annual %)",
    "population in largest city",
    "refugee population by country or territory of asylum",
    "refugee population by country or territory of origin",
    "rural population (% of total population)",
    "urban population (% of total population)",
    "multidimensional poverty headcount ratio (% of total population)",
]

def normalize_lists(i):
    i = [x.replace("%", "prcnt") for x in i]
    i = [x.replace("management", "mgmt") for x in i]
    i = [x.replace("unemployment", "unemploy") for x in i]
    i = [x.replace("female", "fem") for x in i]
    i = [x.replace("of ", "") for x in i]
    i = [remove_special_characters(x) for x in i]
    i = [x.replace(" ", "_") for x in i]
    i = [x.replace("__", "_") for x in i]
    i = [x.replace("multidimensional ", "") for x in i]
    i = [x.replace("performance", "perf") for x in i]
    i = [x.replace('time_spent_dealing_with_the_requirements_government_regulations_prcnt_senior_mgmt_time','time_dealing_with_government_regulations_prcnt_senior_mngmnt') for x in i]
    i = [x.replace('cause_death_by_communicable_diseases_and_maternal_prenatal_and_nutrition_conditions_prcnt_total','death_by_communicable_diseases_prcnt_total') for x in i]
    i = [x.replace('male_mortality_between_age_15_and_50_deaths_under_age_50_per_1000_males_alive_at_age_15','male_mortality_between_15_and_50_per_1000_15_yold_males') for x in i]
    i = [x.replace('fem_mortality_between_age_15_and_50_deaths_under_age_50_per_1000_fems_alive_at_age_15','fem_mortality_between_15_and_50_per_1000_15_yold_fems') for x in i]
    i = [x.replace('domestic_general_government_health_expenditure_per_capita_current_us','government_health_expenditure_per_capita_current_us') for x in i]
    i = [x.replace('people_using_at_least_basic_drinking_water_services_prcnt_population','access_basic_drinking_water_services_prcnt_population') for x in i]
    i = [x.replace('people_with_basic_handwashing_facilities_including_soap_and_water_prcnt_population','access_basic_handwashing_facilities_prcnt_population') for x in i]
    i = [x.replace('prevalence_moderate_or_severe_food_insecurity_in_the_population_prcnt','prevalence_food_insecurity_in_the_population_prcnt') for x in i]
    i = [x.replace('educational_attainment_at_least_bachelors_or_equivalent_population_25_total_prcnt_cumulative','educational_attainment_bachelor_total_prcnt_cumulative') for x in i]
    i = [x.replace('educational_attainment_at_least_completed_lower_secondary_population_25_total_prcnt_cumulative','educational_attainment_lowersecondary_total_prcnt_cumulative') for x in i]
    i = [x.replace('educational_attainment_at_least_completed_upper_secondary_population_25_total_prcnt_cumulative','educational_attainment_uppersecondary_total_prcnt_cumulative') for x in i]
    i = [x.replace('educational_attainment_at_least_masters_or_equivalent_population_25_total_prcnt_cumulative','educational_attainment_masters_total_prcnt_cumulative') for x in i]
    i = [x.replace('educational_attainment_doctoral_or_equivalent_population_25_total_prcnt_cumulative','educational_attainment_doctoral_total_prcnt_cumulative') for x in i]
    i = [x.replace('employment_in_agriculture_prcnt_total_employment_modeled_ilo_estimate','employment_in_agriculture_prcnt_total_employment_estimate') for x in i]
    i = [x.replace('employment_in_industry_prcnt_total_employment_modeled_ilo_estimate','employment_in_industry_prcnt_total_employment_estimate') for x in i]
    i = [x.replace('employment_in_services_prcnt_total_employment_modeled_ilo_estimate','employment_in_services_prcnt_total_employment_estimate') for x in i]
    return i



economia = normalize_lists(economia)
salud = normalize_lists(salud)
educacion = normalize_lists(educacion)
empleos = normalize_lists(empleos)
poblacion = normalize_lists(poblacion)