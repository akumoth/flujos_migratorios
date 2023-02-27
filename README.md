[*Cookiecutter Data Science*]: https://drivendata.github.io/cookiecutter-data-science/ "Cookiecutter Data Science" 

[*International Migrant Stock*]: https://www.un.org/development/desa/pd/content/international-migrant-stock  "International Migrant Stock 2020 - World Bank"
[*Statistical Capacity Indicators*]: https://databank.worldbank.org/source/statistical-capacity-indicators "Statistical Capacity Indicators"
[*DataBank*]: https://databank.worldbank.org/ "World Bank DataBank"
[*World Development Indicators*]: https://databank.worldbank.org/source/world-development-indicators "World Development Indicators - World Bank"
[*World Population Prospects*]: https://www.un.org/development/desa/pd/content/World-Population-Prospects-2022 "World Population Prospects 2022"
[*Jupyter Notebook*]: https://docs.jupyter.org/en/latest/running.html "Jupyter Docs | Running the Notebook"
# Flujos Migratorios

Dashboard y analísis de diversos conjuntos de datos con el fin de contextualizar los flujos migratorios que ocurren entre los países del globo, e indagar acerca de sus causas y sus consecuencias.

# ¿Porque tratar este problema?

Los flujos migratorios son un fenómeno social y demográfico que se refiere al movimiento de personas de un lugar a otro. Estos movimientos pueden ser motivados por diversas razones, como la búsqueda de trabajo, estudios, reunificación familiar, huida de conflictos políticos o violencia, entre otros.
Los flujos migratorios han sido una constante en la historia de la humanidad y han sido moldeados por factores económicos, políticos, sociales y culturales. En la actualidad, son cada vez más frecuentes y han adquirido una importancia significativa en el contexto de la globalización.
La comprensión de los flujos migratorios es crucial para entender los retos y oportunidades que plantea la movilidad humana a nivel local, nacional e internacional. Por esta razón, resulta importante analizar sus causas, patrones y consecuencias, así como las políticas y medidas que se pueden implementar para hacer frente a sus desafíos y aprovechar sus beneficios.

# Ejecución del proyecto

Nuestro proyecto tiene tres partes: 
* Para ver los **notebook** donde analizamos los conjuntos iniciales de datos y graficamos algunos indicadores, instale los paquetes de python utilizados en estos archivos ejecutando `pip install -r requirements.txt` en una terminal, y después simplemente abralos utilizando [*Jupyter Notebook*].
* Para crear las tablas con **MySQL**, y posteriormente cargar los datos ahí, instale los paquetes como fue anteriormente descrito, y después ejecute `python create_database.py [Nombre de su base de datos] [Nombre de usuario] [Contraseña] [Host] [Puerto (opcional)]` dentro de la carpeta *flujos_migratorios*. Esto creara un archivo llamado `peewee_models.py` en la misma carpeta (tenga cuidado, ya que contendrá la contraseña anteriormente utilizada), a través del cual podrá ingestar los datos utilizando `python update_database.py`.
* Para ver el **dashboard** con el cual se visualizaron y analizaron los datos, abra el archivo `powerbimodel.pbix` dentro de la carpeta *flujos_migratorios/dashboard*.

**Analísis exploratorio de los datos**

### Estructura de los archivos del repositorio

Basada en el proyecto [*Cookiecutter Data Science*], para acercarse lo más posible a un esquema universal, accesible y facíl de entender. Nuestros archivos los hemos organizado de la siguiente manera:

* **datasets** - Carpeta en la que se guardan los conjuntos de datos con los que trabajamos, y de donde se cargan los archivos en nuestros scripts y dashboards.
* * datasets/**raw** - Datos brutos en el formato (csv o xlsx) en el que fueron encontrados originalmente.
* * datasets/**processed** - Datos después de ser llevados por un proceso de limpieza, normalización o estandarización. La mayoría tienen el mismo nombre que su contraparte en bruto, pero algunos están divididos según ciertas categorias o tienen información adicional que se le ha añadido utilizando scripts.
* * datasets/**sql** - Datos puestos en el formato de las tablas de sql, después de ser procesados mediantes los scripts de ETL.

Dentro de las *raw*, *processed* y *sql*, encontramos otras subcarpetas, una por cada sitio o analísis origen del cual se extrayeron los datos:

* * * datasets/raw/**proyecto_poblacion** - Datos extraidos de la ultima revisión del reporte [*International Migrant Stock*] disponible durante la realización de este proyecto. En estos conjuntos de datos juntados por la UN se encuentra la información pertinente a desplazamiento de poblaciones entre países: numeros totales de poblaciones por país a nivel mundial, y de migraciones/inmigraciones desde/hacía los países con información publica y accesible.
* * * datasets/raw/proyecto_poblacion/**top_16** - De la anterior carpeta, datos preprocesados donde se da por año el desplazamiento total de habitantes desde/hacía el top 16 de los países, seleccionados a partir de su numero de migrantes/immigrantes.
 
* * * datasets/raw/**statistical_capacity_indicators** - Datos extraidos del DataBank del The World Bank. En este caso, se utilizaron los [*Statistical Capacity Indicators*] delineados en aquel portal, en el cual se muestran indicadores relacionados con la calidad de salud y las condiciones economicas de cada país.

* * * datasets/raw/**world_bank_data** - Datos extraidos del [*DataBank*] del The World Bank. Estos conjuntos fueron extraidos de esta fuente filtrando por los indicadores que encontramos pertinentes a nuestra investigación. Por orden alfabetico: *energia_sostenible* tiene información respecto al acceso a la electricidad y combustibles limpios, *informacion_general* tiene un numero de campos relacionados a las condiciones economicas, legales y laborales, y *precio_de_remesas* cataloga el precio promedio de mandar remesas desde un determinado país (para aquellos que disponibilizan los datos).

* * * datasets/raw/**world_development_indicators** - Datos extraidos del DataBank del The World Bank. En este ultimo conjunto, se filtraron los datos bajo los [*World Development Indicators*] delineados en aquel portal. Estos indicadores contienen una gran cantidad de información relacionada con el desarrollo economico y tecnologico de cada país.

* * * datasets/raw/**world_population_prospects** - Datos extraidos de la ultima revisión del reporte [*World Population Prospects*] disponible durante la realización de este projecto. En este conjunto de datos juntados por la UN se encuentran organizadas por año de estudio las tasas de natalidad y mortalidad de cada país, su población, y su tasa neta de migrantes. 

* **flujos_migratorios** - Carpeta principal del proyecto. Aquí se encuentran los scripts con los cuales se pueden generar los datos procesados, ingestar información a la base de datos, y demás funciones por definir.
* * flujos_migratorios/**dashboard** - Carpeta del dashboard del proyecto. 

* **notebook** - Notebooks de Jupyter. En esta carpeta raíz se encuentran los EDA realizados, con el mismo nombre que la fuente de los datos que fueron trabajados.
* notebook/**normalizacion** - Notebooks de Jupyter donde se detalla el proceso de normalización, división y filtración de los distintos conjuntos de datos.

