import csv
import sys


def create_dummy_data(population=100):
    """
    write dummy data in 'dummy_data.csv'
    """
    with open('dummy_data.csv', mode='w') as data_file:
        number_population = population

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


def main():
    """
    running create_dummy_data in terminal
    """
    if len(sys.argv) > 2:
        print('\nuse >>> python3 create_csv_randomdata.py <population>'
            '\nor for population=100 >>> python3 create_csv_randomdata.py')
        sys.exit(1)
    
    population = 100
    if len(sys.argv) == 2:
        try:
            population = int(sys.argv[1])
        except:
            print("population should be integer")

    if population:
        create_dummy_data(population=population)
    else:
        create_dummy_data()
    return print(f"file dummy_data.csv with {population} population has been created!")


if __name__ == "__main__":
    main()

