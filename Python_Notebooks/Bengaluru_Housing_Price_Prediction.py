#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
matplotlib.rcParams["figure.figsize"] = (20,10)


# In[2]:


df = pd.read_csv('C:\\Personal\\Projects\\Datasets\\Bengaluru_House_Price\\Bengaluru_House_Data.csv')
df.head(10)


# In[3]:


df.shape


# In[4]:


df.groupby(['area_type','size'])['area_type'].agg('count')


# In[5]:


# Removed unwanted features
df2 =  df.drop(['area_type','availability','society'], axis = 'columns')
df2.head(6)


# In[6]:


df2.isnull().sum()


# In[7]:


# After dropping null values
df3 = df2.dropna()
df3.head(10)


# In[8]:


df3.shape


# In[9]:


df3.isna().sum()


# In[10]:


df3['size'].unique()


# In[11]:


df3['BHK'] = df3['size'].apply(lambda x: int(x.split(' ')[0]))


# In[12]:


df3.head()


# In[13]:


# Replacing BHK column for size feature
df4 = df3.drop('size',axis='columns')
df4.head()


# In[14]:


df4[df4.BHK<=3]


# In[15]:


df4['total_sqft'].unique()


# In[16]:


def is_float(x):
    try:
        float(x)
    except:
        return False
    return True


# In[17]:


df4[~df4.total_sqft.apply(lambda x: is_float(x))].head()


# In[18]:


def convert_sqft_into_nums(x):
    x_split = x.split('-')
    if len(x_split) == 2:
        return float(float(x_split[0]) + float(x_split[1]))/2
    try:
        return float(x)
    except:
        return None


# In[19]:


df4['total_sqft'] = df4['total_sqft'].apply(convert_sqft_into_nums)
df4.head()


# In[20]:


df4[~df4.total_sqft.apply(lambda x: is_float(x))].head()


# In[21]:


df5 = df4.copy()
df5.head()


# Feature Engineering

# In[22]:


df5['price_per_sqft'] = round(df5['price'] * 100000 / df5['total_sqft'],2)


# In[23]:


df5.head()


# In[24]:


len(df5.location.unique())


# In[25]:


df5.location = df5.location.apply(lambda x : x.strip())
location_stats = df5.groupby('location')['location'].agg('count').sort_values(ascending = False)
location_stats


# In[26]:


locations_stats_less_than_10 = location_stats[location_stats<=10]


# In[27]:


locations_stats_less_than_10


# In[28]:


df5.location = df5.location.apply(lambda x : "others" if x in locations_stats_less_than_10 else x)


# In[29]:


len(df5.location.unique())


# In[30]:


df5.head(10)


# In[31]:


df5[df5.location == 'others']


# Removal of Outliers

# In[32]:


# unusual number of bedrooms
df5[df5.total_sqft / df5.BHK <= 300]


# In[33]:


#Removing unusual number of bedrooms
df6 =  df5[~(df5.total_sqft / df5.BHK <= 300)]
# df6.loc[58]
df6.shape


# In[34]:


df5.shape


# In[35]:


def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    # As the price will vary for each location/area, it is split into groups of locations
    for key, subdf in df.groupby('location'):
        mean = np.mean(subdf.price_per_sqft)
        sd = np.std(subdf.price_per_sqft)
        # filter only the records where the price per sqft comes under the std-1 (normal distribution)
        reduced_df = subdf[(subdf.price_per_sqft > (mean-sd)) & (subdf.price_per_sqft <= (mean+sd))]
        df_out = pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out


# In[36]:


# Outliers were Removed
df7 = remove_pps_outliers(df6)
df7.head()


# In[37]:


def plot_scattter_plot(df,location):
    bhk2 = df[(df.location == location) & (df.BHK==2)]
    bhk3 = df[(df.location == location) & (df.BHK==3)]
    matplotlib.rcParams['figure.figsize'] = (15,10)
    plt.scatter(bhk2.total_sqft,bhk2.price,marker='+',color='green',label='2 BHK',s=50)
    plt.scatter(bhk3.total_sqft,bhk3.price,marker='o',color='blue',label='3 BHK',s=50)
    plt.xlabel('Total Square Feet Area')
    plt.ylabel('Price')
    plt.title(location)
    plt.legend()

plot_scattter_plot(df7,'Hebbal')


# In[38]:


def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('BHK'):
            bhk_stats[bhk]={
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count':bhk_df.shape[0]
            }
        for bhk,bhk_df in location_df.groupby('BHK'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis = 'index')


# In[39]:


df8 = remove_bhk_outliers(df7)
df8.head()


# In[40]:


plot_scattter_plot(df8,'Hebbal')


# In[41]:


# Check if it is in normal distrubution (approx).
matplotlib.rcParams['figure.figsize'] = (20,10)
plt.hist(df8.price_per_sqft,rwidth=0.9)
plt.xlabel('Price per Square Feet')
plt.ylabel('Count')


# In[42]:


df8.bath.unique()


# In[43]:


df9 = df8[df8.bath <= (df8.BHK + 2)]
df9.head()


# In[44]:


df9.shape


# In[45]:


df10 = df9.drop(['price_per_sqft'],axis='columns')
df10.head()

