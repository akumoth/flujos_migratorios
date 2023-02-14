import pycountry
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
