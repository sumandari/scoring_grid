import csv
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from scoring_grid.status_score import status_score_km_grid


class PlottingWeighing():
    def __init__(self, population=100):
        self.population = population

    def create_dummy_data(self):
        """
        write dummy data in 'dummy_data.csv'
        """
        with open('dummy_data.csv', mode='w') as data_file:
            number_population = self.population

            data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow(['red', 'yellow', 'green', '%_responder', 'score'])
            
            for red in range(0, number_population + 1):
                for green in range(0, number_population + 1):
                    for yellow in range(0, number_population + 1):
                        total_responder = red + green + yellow
                        if total_responder <= number_population:
                            score = (1 / number_population) * ((5 * red) + (2 * yellow) - green)
                            persen_responder = round(total_responder/number_population, 2)
                            data_writer.writerow([red, yellow, green, persen_responder, score])
        return

    def plot_dummydata(self, file_csv='dummy_data.csv'):
        # read csv
        df = pd.read_csv(file_csv)

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


class PlottingStatus():
    """
    create chart for plotting grid status
    """    
    def __init__(self, population=100, error=0.0, sample=0.1):
        self.population = population
        self.error = error
        self.sample = sample

    def create_status_data(self):
        """
        return csv
        """
        with open('scoring_data.csv', mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter=',', quotechar='"', 
                quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow(['red', 'yellow', 'green', 'status', 'rgb'])
            for red in range(0, self.population + 1):
                for yellow in range(0, self.population +1):
                    for green in range(0, self.population +1):
                        total_responder = red + yellow + green
                        if total_responder <= self.population:
                            status_grid = status_score_km_grid(
                                user_report_green=green,
                                user_report_yellow=yellow,
                                user_report_red=red,
                                population=self.population,
                                error_allowed=self.error,
                                estimated_responden=self.sample
                                )
                            if status_grid == 'red':
                                rgb = 'rgb(255,0,0)'
                            elif status_grid == 'green':
                                rgb = 'rgb(0, 255,0)'
                            elif status_grid == 'yellow':
                                rgb = 'rgb(255,255,0)'
                            data_writer.writerow([red, yellow, green, status_grid,rgb])
        return

    def plot_status(self, file_csv='scoring_data.csv'):
        # read csv
        df = pd.read_csv(file_csv)

        trace1 = go.Scatter3d(
            x=df.red,
            y=df.yellow,
            z=df.green,
            text=df.status,
            mode='markers',
            marker=dict(
                size=10,
                color=df.rgb,                # set color to an array/list of desired values      
            ),
            hovertemplate= 
                '<b>status: %{text}</b>' +
                '<br>red: %{x} report' +
                '<br>yellow: %{y} report' +
                '<br>green: %{z} report'+
                '<extra></extra>',
            hoverlabel=dict(
                bgcolor=df.rgb
            ),
        )

        data = [trace1]
        layout = go.Layout(
            title='Population: {}, minimum responder: {}, estimated responder {}'\
                .format(self.population,self.error,self.sample),
            autosize = True,
            scene = dict(
                xaxis = dict(
                    title='red report'),
                yaxis = dict(
                    title='yellow report'),
                zaxis = dict(
                    title='green report'),
            ),
            showlegend=False,
        )

        fig = go.Figure(data=data, layout=layout)

        fig.update_layout(
            title={
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        fig.show()


def main():
    while True:
        mode = input("""
        1. Generate chart for dummy data weighing score
        2. Generate 3D scatter chart for scoring result
        ---
        choose 1 or 2 :""")

        try:
            choice = int(mode)
            if choice in [1, 2]:
                break
            else:
                raise ValueError
        except ValueError:
            print('\ninput should be 1 or 2')
        

    if choice == 1:
        print(""" 
            Generate chart for dummy data weighing score
            ============================================
        """)
        while True:
            population = input('Population: ')

            try:
                population = int(population)
                break
            except ValueError:
                print('\npopulation should be integer!')

        plotting = PlottingWeighing(population=population)
        
        plotting.create_dummy_data()
        print('file dummy_data.csv created. Waiting for your chart...')
        
        plotting.plot_dummydata()
        print('plot figure successfully generated!\n')

    
    elif choice == 2:
        print(""" 
            Generate 3D scatter chart for scoring result
            ============================================
        """)
        while True:
            population = input('population (integer): ')
            error_allowed = input('error allowed (decimal): ')
            sample = input('% responder of population (decimal): ')
            
            try:
                population = int(population)
            except ValueError:
                print('\npopulation should be integer!')

            try:
                error_allowed = float(error_allowed)
                sample = float(sample)
                break
            except ValueError:
                print('\nerror allowed and % responder of population should be decimal!')

        
        plotting = PlottingStatus(population=population, 
            error=error_allowed, 
            sample=sample)
        plotting.create_status_data()
        print('file scoring_data.csv created. Waiting for your chart...')
        
        plotting.plot_status()
        print('plot figure successfully generated!\n')

if __name__ == "__main__":
    main()     
