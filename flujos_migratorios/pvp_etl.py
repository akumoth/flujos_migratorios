import pandas as pd
import numpy as np
import etl
import varname

# Carga inicial de los conjuntos de datos.
# Al realizar su normalización inicial, se detallaron ciertas columnas que serían inutiles para nuestra base de datos, 
# las cuales quitamos al cargar.

total_pvp = pd.read_csv('../datasets/processed/proyecto_poblacion/total_pvp.csv').drop(['Unnamed: 0','Index','Notes of destination','Location code of destination','Type of data of destination','Location code of origin'],axis=1)
male_pvp = pd.read_csv('../datasets/processed/proyecto_poblacion/male_pvp.csv').drop(['Unnamed: 0','Index','Notes of destination','Location code of destination','Type of data of destination','Location code of origin'],axis=1)
fem_pvp = pd.read_csv('../datasets/processed/proyecto_poblacion/fem_pvp.csv').drop(['Unnamed: 0','Index','Notes of destination','Location code of destination','Type of data of destination','Location code of origin'],axis=1)

# Estandarización del formato de los conjuntos de datos:

def pvp_normalization(df):
    # Empezando por las propias columnas, y después quitando caracteres especiales y espacios en blancos excesivos.
    df.columns = ['destination','origin','1990','1995','2000','2005','2010','2015','2020']

    for j in ['destination', 'origin']:
        df[j] = df[j].apply(etl.remove_special_characters).str.lower()
        df[j] = df[j].astype(str)
        df[j] = df[j].str.strip()
        df[j] = df[j].apply(etl.normalize_country).str.lower()
        # Después, quitamos aquellas filas que correspondan a países que no se encuentran dentro de nuestro modelo.
        df = df.drop(df.where(~df[j].isin(etl.country_code_df['name'])).dropna().index,axis=0)

    # Finalmente, agregamos las columnas 'destination_id' y 'origin_id', que se enlazaran mediante una clave foranea
    # a la tabla 'Region' dentro de nuestro modelo.

    etl.insert_country_code(df,'destination','destination_id')
    etl.insert_country_code(df,'origin','origin_id')
    df.insert(1,'destination_id',df.pop('destination_id'))
    df.insert(3,'origin_id',df.pop('origin_id'))

    # Exportación del estado actual del df a un csv
    df.to_csv(f'../datasets/processed/proyecto_poblacion/{varname.nameof(df)}_codigo_pais.csv')

    # Pivoteo para que quedé del mismo formato que la tabla SQL, volviendo el año una columna
    df = (
        df.set_index(["destination", "destination_id", "origin", "origin_id"])
        .rename_axis("year", axis=1)
        .stack()
        .reset_index()
        .sort_values(['year','destination'])
        .rename({0:f'migrants'},axis=1)
        .reset_index(drop=True)
        .rename_axis(None, axis=1)
        .rename_axis("id")
    )
    
    # Dejando unicamente las columnas destination_id para que entren más uniforme dentro al modelo
    df = df.drop(['destination','origin'],axis=1).rename({'destination_id':'destination','origin_id':'origin'},axis=1)
    return df

# La función definida anteriormente la utilizamos para normalizar los dataframes. Después, la tabla 'migrants' de
# male_pvp y fem_pvp la insertamos dentro de total_pvp, y almacenamos esta información dentro de un csv que se
# impotará después en la base de datos SQL
total_pvp = pvp_normalization(total_pvp)
male_pvp = pvp_normalization(male_pvp)
fem_pvp = pvp_normalization(fem_pvp)
total_pvp.insert(4,'male',male_pvp.migrants)
total_pvp.insert(5,'fem',fem_pvp.migrants)
total_pvp.to_csv('../datasets/sql/migration.csv')