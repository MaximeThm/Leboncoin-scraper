import pylbc
import pandas as pd
from datetime import date

print('Minimum desired surface area ?')
min_square = int(input())
print('Maximum desired surface area ?')
max_square = int(input())
print('Minimum price ?')
min_price = int(input())
print('Maximum price ?')
max_price = int(input())

print('City ?')
city = input()
print('ZIP code ?')
zip_code = int(input())

query = pylbc.Search()
query.set_square(min_square, max_square)
query.set_price(min_price, max_price)
query.set_category('locations')
query.set_real_estate_types(['appartement'])
query.add_city(city, zip_code)
query.set_query('')

i = 0
df = pd.DataFrame()

for result in query.iter_results():
    i = i + 1
    data = str(result).split('"')
    df[i] = data

df.drop(df.index[[0, 1, 2, 3, 4, 7, 9, 10, 11, 12]], inplace=True)
df = df.T
df.columns = ['Date', 'Prix', 'Surface']
df['Prix'] = df['Prix'].str[8:11]
df['Surface'] = df['Surface'].str[9:11]

df['Prix'] = df['Prix'].astype(float)
df['Surface'] = df['Surface'].astype(float)
df['Prix/m2'] = df['Prix'] / df['Surface']

df['Ancienneté'] = pd.to_datetime(date.today()) - pd.to_datetime(df['Date'])
df['Date'] = date.today()

print(df.mean(axis=0))
