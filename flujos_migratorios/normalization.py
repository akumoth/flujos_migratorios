import pycountry
import pandas as pd
import numpy as np
import re
from geopy.geocoders import Nominatim

country_code_df = pd.read_csv('../datasets/processed/codigo_pais.csv')
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
    country_code_df.columns = ['region','country_code']
    country_code_df.set_index('region',inplace=True)
    df.insert(df.columns.get_loc("region"),'region_code',df.join(country_code_df,on='region',how='left',validate='m:1')['country_code'])


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