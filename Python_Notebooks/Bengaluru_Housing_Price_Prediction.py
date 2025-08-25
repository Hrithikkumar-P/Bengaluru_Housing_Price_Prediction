# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
# %matplotlib inline
import matplotlib
matplotlib.rcParams["figure.figsize"] = (20,10)

# %%
df = pd.read_csv('C:\\Personal\\Projects\\Datasets\\Bengaluru_House_Price\\Bengaluru_House_Data.csv')
df.head(10)

# %%
df.shape

# %%
df.groupby(['area_type','size'])['area_type'].agg('count')

# %%
# Removed unwanted features
df2 =  df.drop(['area_type','availability','society'], axis = 'columns')
df2.head(6)

# %%
df2.isnull().sum()

# %%
# After dropping null values
df3 = df2.dropna()
df3.head(10)

# %%
df3.shape

# %%
df3.isna().sum()

# %%
df3['size'].unique()

# %%
df3['BHK'] = df3['size'].apply(lambda x: int(x.split(' ')[0]))

# %%
df3.head()

# %%
# Replacing BHK column for size feature
df4 = df3.drop('size',axis='columns')
df4.head()

# %%
df4[df4.BHK<=3]

# %%
df4['total_sqft'].unique()


# %%
def is_float(x):
    try:
        float(x)
    except:
        return False
    return True


# %%
df4[~df4.total_sqft.apply(lambda x: is_float(x))].head()


# %%
def convert_sqft_into_nums(x):
    x_split = x.split('-')
    if len(x_split) == 2:
        return float(float(x_split[0]) + float(x_split[1]))/2
    try:
        return float(x)
    except:
        return None


# %%
df4['total_sqft'] = df4['total_sqft'].apply(convert_sqft_into_nums)
df4.head()

# %%
df4[~df4.total_sqft.apply(lambda x: is_float(x))].head()

# %%
