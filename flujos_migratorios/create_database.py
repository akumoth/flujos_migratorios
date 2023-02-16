import pandas as pd
import sqlite3
import peewee as pw
import normalization
from sqlite3 import Error
from playhouse.migrate import *

db = pw.SqliteDatabase("sql.db")
migrator = SqliteMigrator(db)
country_code_df = pd.read_csv('../datasets/processed/codigo_pais.csv')

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

create_connection("sql.db")

economia = [
    'adjusted net national income (current us$)',
    'adjusted net national income per capita (annual % growth)',
    'adjusted savings: gross savings (% of gni)',
    'cost of business start-up procedures (% of gni per capita)',
    'cost of business start-up procedures, female (% of gni per capita)',
    'cost of business start-up procedures, male (% of gni per capita)',
    'domestic credit to private sector by banks (% of gdp)',
    'domestic credit to private sector (% of gdp)',
    'ease of doing business score (0 = lowest performance to 100 = best performance)',
    'foreign direct investment, net (bop, current us$)',
    'gdp (current us$)',
    'gdp growth (annual %)',
    'gini index',
    'gni (current us$)',
    'gni growth (annual %)',
    'gross domestic savings (current us$)',
    'gross domestic savings (% of gdp)',
    'gross savings (% of gdp)',
    'gross savings (% of gni)',
    'industry (including construction), value added (% of gdp)',
    'industry (including construction), value added (annual % growth)',
    'inflation, consumer prices (annual %)',
    'investment in ict with private participation (current us$)',
    'labor force, total',
    'labor tax and contributions (% of commercial profits)',
    'listed domestic companies, total',
    'market capitalization of listed domestic companies (current us$)',
    'market capitalization of listed domestic companies (% of gdp)',
    'multidimensional poverty headcount ratio (% of total population)',
    'net trade in goods and services (bop, current us$)',
    'new business density (new registrations per 1,000 people ages 15-64)',
    'new businesses registered (number)',
    'personal remittances, received (current us$)',
    'personal remittances, received (% of gdp)',
    'personal remittances, paid (current us$)',
    'profit tax (% of commercial profits)',
    'research and development expenditure (% of gdp)',
    'researchers in r&d (per million people)',
    'tax payments (number)',
    'tax revenue (% of gdp)',
    'taxes on income, profits and capital gains (% of total taxes)',
    'time spent dealing with the requirements of government regulations (% of senior management time)',
    'unemployment, total (% of total labor force) (national estimate)',
    'unemployment, total (% of total labor force) (modeled ilo estimate)'
]

salud = [
    'cause of death, by communicable diseases and maternal, prenatal and nutrition conditions (% of total)',
    'cause of death, by non-communicable diseases (% of total)',
    'death rate, crude (per 1,000 people)',
    'domestic private health expenditure per capita (current us$)',
    'domestic general government health expenditure per capita (current us$)',
    'intentional homicides (per 100,000 people)',
    'life expectancy at birth, total (years)',
    'people using at least basic drinking water services (% of population)',
    'people with basic handwashing facilities including soap and water (% of population)',
    'pregnant women receiving prenatal care (%)',
    'prevalence of moderate or severe food insecurity in the population (%)',
    'suicide mortality rate (per 100,000 population)'
]

educacion = [
    "educational attainment, at least bachelor's or equivalent, population 25+, total (%) (cumulative)",
    'educational attainment, at least completed lower secondary, population 25+, total (%) (cumulative)',
    'educational attainment, at least completed upper secondary, population 25+, total (%) (cumulative)',
    "educational attainment, at least master's or equivalent, population 25+, total (%) (cumulative)",
    'educational attainment, doctoral or equivalent, population 25+, total (%) (cumulative)',
    'technicians in r&d (per million people)'
]

empleos = [
    'employers, total (% of total employment) (modeled ilo estimate)',
    'employment in agriculture (% of total employment) (modeled ilo estimate)',
    'employment in industry (% of total employment) (modeled ilo estimate)',
    'employment in services (% of total employment) (modeled ilo estimate)',
    'firms offering formal training (% of firms)',
    'self-employed, total (% of total employment) (modeled ilo estimate)',
    'time required to start a business (days)',
    'time required to register property (days)',
    'time required to start a business, female (days)',
    'time required to start a business, male (days)',
    'labor force, total',
    'unemployment, total (% of total labor force) (national estimate)',
    'unemployment, total (% of total labor force) (modeled ilo estimate)'
]

poblacion = [
    'individuals using the internet (% of population)',
    'international migrant stock, total',
    'international migrant stock (% of population)',
    'net migration',
    'population ages 0-14 (% of total population)',
    'population density (people per sq. km of land area)',
    'population growth (annual %)',
    'population in largest city',
    'population in the largest city (% of urban population)',
    'population, total',
    'refugee population by country or territory of asylum',
    'refugee population by country or territory of origin',
    'rural population (% of total population)',
    'rural population growth (annual %)',
    'urban population (% of total population)',
    'urban population',
    'urban population growth (annual %)',
    'multidimensional poverty headcount ratio (% of total population)'
 ]

economia = [i.replace("%","percent") for i in economia]
economia = [normalization.remove_special_characters(i) for i in economia]
economia = [i.replace(" ","_") for i in economia]

salud = [i.replace("%","percent") for i in salud]
salud = [normalization.remove_special_characters(i) for i in salud]
salud = [i.replace(" ","_") for i in salud]

educacion = [i.replace("%","percent") for i in educacion]
educacion = [normalization.remove_special_characters(i) for i in educacion]
educacion = [i.replace(" ","_") for i in educacion]

empleos = [i.replace("%","percent") for i in empleos]
empleos = [normalization.remove_special_characters(i) for i in empleos]
empleos = [i.replace(" ","_") for i in empleos]


poblacion = [i.replace("%","percent") for i in poblacion]
poblacion = [normalization.remove_special_characters(i) for i in poblacion]
poblacion = [i.replace(" ","_") for i in poblacion]

class BaseModel(pw.Model):
    class Meta:
        database = db
        table_name = 'migration'

class Region(BaseModel):
    name = pw.CharField()

class Demography(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region)
    
class Health(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region)

class Economy(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region)

class Education(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region)

class Employment(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region)


db.connect()

db.create_tables([Region, Demography, Health, Economy, Education, Employment])

myfield = pw.FloatField(null=True)

for i in economia:
    migrate(
        migrator.add_column('Economy',i,myfield)
    )
for i in salud:
    migrate(
        migrator.add_column('Health',i,myfield)
    )
for i in educacion:
    migrate(
        migrator.add_column('Education',i,myfield)
    )
for i in empleos:
    migrate(
        migrator.add_column('Employment',i,myfield)
    )
for i in poblacion:
    migrate(
        migrator.add_column('Demography',i,myfield)
    )

country_code_df = country_code_df.set_index('cod')
country_code_df.columns = ['name']

Region.insert_many(country_code_df.to_dict(orient="records")).execute()

import os

os.system("python -m pwiz sql.db > peewee_models.py")