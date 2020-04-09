import sys

def status_score_km_grid(
        user_report_green = 0,
        user_report_yellow = 0,
        user_report_red = 0,
        error_allowed = .05,
        population = 0
    ):
    """
    scoring km_grid based on count of user report
    return : status km_grid red / yellow / green
    return type: string
    """
    number_of_sample = user_report_green + user_report_yellow + user_report_red
    
    if population <= 0:
        return 'green'

    if number_of_sample < population * error_allowed:
        return 'green'

    score = (1 / population) * \
            ((5 * user_report_red) + (2 * user_report_yellow) - user_report_green)

    if score < 0.4:
        status_score = 'green'
    elif 0.4 <= score <= 0.6:
        status_score = 'yellow'
    elif score > 0.6:
        status_score = 'red'
    return status_score


def main():
    """
    running status_score_km_grid in terminal
    """
    if len(sys.argv) != 5:
        print('\nuse >>> python3 status_score.py <count_green> <count_yellow> <count_red> <population>')
        sys.exit(1)
    try:
        count_green = int(sys.argv[1])
        count_yellow = int(sys.argv[2])
        count_red = int(sys.argv[3])
        population = int(sys.argv[4])
    except:
        print("parameters should be integer")

    status = status_score_km_grid(
        user_report_green = count_green,
        user_report_yellow = count_yellow,
        user_report_red = count_red,
        population = population
    )
    return print(status)


if __name__ == "__main__":
    main()