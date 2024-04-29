
#%% [markdown]
# Imports
import pandas as pd
import os

# %% [markdown]
# Read data
df = pd.read_csv('ex1.csv')

#%% merfe first row into columns
df.columns = df.columns.str.cat(df.iloc[0], sep='_')
df = df.drop(0)

#%% [markdown]
# Fix column names
df.columns = ['Country', 'Region', *df.columns[2:]]

# %% [markdown]
# Start clean dataframe
df_clean = df.copy()

# %% [markdown]
# Fill nulls
df_clean['IMF_Forecast'] = df_clean['IMF_Forecast'].replace('—',pd.NA)
df_clean['World Bank_Estimate'] = df_clean['World Bank_Estimate'].replace('—',pd.NA)
df_clean['United Nations_Estimate'] = df_clean['United Nations_Estimate'].replace('—',pd.NA)

df_clean['GDP'] = df_clean['IMF_Forecast'].fillna(df_clean['World Bank_Estimate'])

#%% [markdown]
# Check nulls
df_clean.isna().sum()

#%% [markdown]
# Fix nulls
df_clean['GDP'] = df_clean['GDP'].fillna(df_clean['United Nations_Estimate'])

#%% [markdown]
# Check nulls
df_clean.isna().sum()

# %% [markdown]
# Final cleanup
df_clean['GDP'] = df_clean['GDP'].str.replace(',', '').astype('float')
df_clean = df_clean[['Country', 'Region', 'GDP']]

# %% [markdown]
# Save to file
df_clean.to_csv('ex1_clean.csv', index=False)

# %% [markdown]
# Questions


#%% [markdown]
#Take out World
df_clean = df_clean.loc[~(df_clean.Country == 'World')]

#%% [markdown]
# Compute GDP and sort
total_gdp = df_clean['GDP'].sum()
df_clean['GDP_pcg'] = df_clean['GDP'] / total_gdp * 100
df_clean = df_clean.sort_values('GDP_pcg', ascending=False).reset_index(drop=True)

#%% [markdown]
#### 1. What is Greece's GDP and how much of the world's GDP does it represent?
df_clean.loc[df_clean.Country == 'Greece']

# %% [markdown]
#### 2. What is the ranking of Greece in the World?
df_clean['Global_rank'] = df_clean['GDP'].rank(method='min', ascending=False)
df_clean.loc[df_clean.Country == 'Greece']

# %% [markdown]
#### 3. Repeat 1 and 2 only considering Europe
df_clean_eur = df_clean.loc[df_clean.Region == 'Europe'].copy()
total_gdp = df_clean_eur['GDP'].sum()
df_clean_eur['Region_GDP_pcg'] = df_clean_eur['GDP'] / total_gdp * 100
df_clean_eur = df_clean_eur.sort_values('Region_GDP_pcg', ascending=False).reset_index(drop=True)
df_clean_eur['Region_rank'] = df_clean_eur['GDP'].rank(method='min', ascending=False)

df_clean_eur.loc[df_clean_eur.Country == 'Greece']

# %% [markdown]
#### General solution
df_clean['Region_GDP_sum'] = df_clean.groupby('Region')['GDP'].transform('sum')
df_clean['Region_GDP_pcg'] = 100*df_clean['GDP']/df_clean['Region_GDP_sum']
df_clean['Region_rank'] = df_clean.groupby('Region')['GDP'].rank('min', ascending=False)

#%% Example
df_clean.loc[df_clean.Country == 'Greece']

#%% Example
df_clean.loc[df_clean.Country == 'Japan']

# %% [markdown]
#### 4. Get the last country for each region
df_clean.groupby('Region').apply(lambda x: x.loc[x['Region_rank'].idxmax()])


# %% [markdown]
#### 5. Get the fifth country in each region
df_clean.groupby('Region').apply(lambda x: x.loc[x['Region_rank']==5.0])