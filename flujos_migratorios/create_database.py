import pandas as pd
import peewee as pw
import etl
import sys
from playhouse.migrate import *
import time

# Definición de la base de datos y nuestra conexión a ella

if len(sys.argv) < 4:
    print('Not enough arguments!\n usage: python create_database.py [MySQL DB name] [username] [password] [host]')
    exit()

db = pw.MySQLDatabase(sys.argv[1], user=sys.argv[2], password=sys.argv[3],
                         host=sys.argv[4], port=3306)

migrator = MySQLMigrator(db)

# Creación del modelo de la base de datos, utilizando una clase por tabla 

class BaseModel(pw.Model):
    class Meta:
        database = db
        table_name = 'migration'

class Region(BaseModel):
    name = pw.CharField()
    lang = pw.CharField()
    lat = pw.FloatField(null=True)
    long = pw.FloatField(null=True)

class Migration(BaseModel):
    year = pw.IntegerField()
    destination = pw.ForeignKeyField(Region, null=True)
    origin = pw.ForeignKeyField(Region, null=True)
    migrants = pw.IntegerField(null=True)
    fem = pw.IntegerField(null=True)
    male = pw.IntegerField(null=True)

class Demography(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region, default=None, null=True)
    
class Health(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region, default=None, null=True)

class Economy(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region, default=None, null=True)

class Education(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region, default=None, null=True)

class Employment(BaseModel):
    year = pw.IntegerField()
    region = pw.ForeignKeyField(Region, default=None, null=True)

# Conexión y creación de las tablas

db.connect()

db.drop_tables((Demography, Region, Health, Economy, Education, Employment, Migration))

db.create_tables([Region])
Region.insert_many(etl.country_code_df.set_index('cod').to_dict(orient="records")).execute()

db.create_tables([Demography, Health, Economy, Education, Employment, Migration])
myfield = pw.FloatField(null=True)

time.sleep(5)

# Creando cada uno de los campos relevantes en las tablas, como están definidas en el archivo etl.py

for i in etl.economia:
    migrate(
        migrator.add_column('economy',i,myfield)
    )
for i in etl.salud:
    migrate(
        migrator.add_column('health',i,myfield)
    )
for i in etl.educacion:
    migrate(
        migrator.add_column('education',i,myfield)
    )
for i in etl.empleos:
    migrate(
        migrator.add_column('employment',i,myfield)
    )
for i in etl.poblacion:
    migrate(
        migrator.add_column('demography',i,myfield)
    )


import os

# Ejecutando el script de pwiz que genere automaticamente un modulo que cargué las tablas en la base de datos

os.system(f"python -m pwiz -e mysql -u {sys.argv[2]} -P {sys.argv[1]} -H {sys.argv[4]} > peewee_models.py")

db.close()