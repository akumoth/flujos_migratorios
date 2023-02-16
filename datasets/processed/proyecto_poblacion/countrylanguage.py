import pandas as pd
import pycountry
import pycountry_convert as pc
# Cargar el dataframe con la columna de países
df = pd.read_csv('./top_16/top_16_destino_promedio.csv')

df['Region, development group, country or area'] = df['Region, development group, country or area'].str.strip()
df['Region, development group, country or area'] = df['Region, development group, country or area'].replace({"Côte d'Ivoire" : "cote d'ivoire"})
df['Region, development group, country or area'] = df['Region, development group, country or area'].replace({"Spain*": "spain"})

def normalize_country(name):
    custom_mapping = {
        "spain*": "spain",
        "Iran (Islamic Republic of)": "iran",
        "côte d'ivoire": "cote d'ivoire",
        "China, Hong Kong SAR*": "hong kong",
        "hong kong sar, china": "hong kong",
        "iran, islamic rep.": "iran",
        "turkey":"turkiye",
        "United States of America*": "United States",
        "Iran (Islamic Republic of)": "iran",
        "Russian Federation": "russia",
        "France*": "France",
        "Australia*": "Australia",
        "United Kingdom*": "United Kingdom",
        "China, Hong Kong SAR*": "hong kong", 
        "Ukraine*": "Ukraine"
    }
    
    if name in custom_mapping:
        return custom_mapping[name]
    
    # Buscar el país más cercano al nombre normalizado
    country = pycountry.countries.search_fuzzy(name)
    if country:
        return country[0].name
    else:
        return name

df['Region, development group, country or area'] = df['Region, development group, country or area'].apply(normalize_country).str.lower()

import geonamescache

def obtener_idioma_principal(pais):
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    for codigo, detalles in countries.items():
        if detalles['name'] == str.capitalize(pais):
            idioma_principal = detalles['languages'][0]
            return idioma_principal
    return None


df['idioma_principal'] = df['Region, development group, country or area'].apply(obtener_idioma_principal)

def obtener_idioma_principal(pais):
    try:
        pais_normalizado = normalize_country(pais)
        pais_alpha2 = pc.country_name_to_country_alpha2(pais_normalizado, cn_name_format="default")
        idiomas = pc.country_alpha2_to_languages(pais_alpha2)
        if idiomas:
            return idiomas[0]
        else:
            return None
    except:
        return None

# Agregar los idiomas principales al dataframe
df['idioma_principal'] = df['Region, development group, country or area'].apply(obtener_idioma_principal)