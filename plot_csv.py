import pandas as pd
import plotly.express as px

# read csv
df = pd.read_csv('dummy_data.csv')

# get number of population
find_data = df.loc[df['%_responder'].idxmax()]
number_population = find_data['red'] + find_data['yellow'] + find_data['green']
number_population = int(number_population)

# draw plot
fig = px.scatter(df, 
    x = '%_responder', 
    y = 'score', 
    title=f'scoring = 5red + 2yellow - green, number of population: {number_population}',
    hover_data=['red', 'yellow', 'green'])
fig.show()