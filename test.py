import pandas as pd

bronze_top = pd.read_csv('bronze_top.csv')
silver_top = pd.read_csv('silver_top.csv')

data = bronze_top.merge(silver_top, how='inner', on='Country', suffixes=('bronze', 'silver')) 
print(apply_discounts(products, stocks))