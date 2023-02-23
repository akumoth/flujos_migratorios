import sys
import streamlit as st
import pandas as pd
import inspect
import os
import numpy as np
sys.path.append("../")

from peewee_models import *

def retrieve_name(var):
        """
        Gets the name of var. Does it from the out most frame inner-wards.
        :param var: variable to get name from.
        :return: string
        """
        for fi in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]

economy_df = pd.DataFrame(Economy.select().dicts()).drop('id',axis=1)
region_df = pd.DataFrame(Region.select().dicts()).drop('id',axis=1)
migration_df = pd.DataFrame(Migration.select().dicts()).drop('id',axis=1)
empleos_df = pd.DataFrame(Employment.select().dicts()).drop('id',axis=1)
salud_df = pd.DataFrame(Health.select().dicts()).drop('id',axis=1)
demografia_df = pd.DataFrame(Demography.select().dicts()).drop('id',axis=1)
educacion_df = pd.DataFrame(Education.select().dicts()).drop('id',axis=1)

region_df.index = np.arange(1, len(region_df) + 1)
region_df.reset_index(inplace=True)
region_df = region_df.rename({"index": "region_id"}, axis=1)

namedfs = {'economy_df':'economy_parquet',}
for i in [economy_df, empleos_df, salud_df, demografia_df, educacion_df]:
    pd.merge(i.rename({"region": "region_id"}, axis=1), region_df, on="region_id").to_csv(f'parquet/{retrieve_name(i)}.csv')

os.system(f"streamlit run introduccion.py")
