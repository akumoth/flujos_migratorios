import pandas as pd
import sqlite3
import peewee as pw
import etl
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

for i in etl.economia:
    migrate(
        migrator.add_column('Economy',i,myfield)
    )
for i in etl.salud:
    migrate(
        migrator.add_column('Health',i,myfield)
    )
for i in etl.educacion:
    migrate(
        migrator.add_column('Education',i,myfield)
    )
for i in etl.empleos:
    migrate(
        migrator.add_column('Employment',i,myfield)
    )
for i in etl.poblacion:
    migrate(
        migrator.add_column('Demography',i,myfield)
    )

country_code_df = country_code_df.set_index('cod')
country_code_df.columns = ['name']

Region.insert_many(country_code_df.to_dict(orient="records")).execute()

import os

os.system("python -m pwiz sql.db > peewee_models.py")