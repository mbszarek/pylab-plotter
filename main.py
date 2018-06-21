from plotter import Plotter


def first_menu(optional: int):
    if optional == 1:
        print("1 to display countries by goals scored\n2 to display countries by appearances\n3 to display countries "
              "with most wins\n4 to display countries with best win-ratio\n")
    elif optional == 2:
        print("1 to display country goals by years\n2 to display country appearances by year\n3 to display countries "
              "wins by years\n4 to display country win-ratio by year\n")
    return_val = input("Input: ")
    if return_val == '':
        raise ValueError
    return int(return_val)


def statistics_menu(optional: int):
    amount = input("How many countries: ")
    if amount == '':
        raise ValueError
    amount = int(amount)
    if optional == 1:
        plotter.plot_countries_with_most_goals(amount)
    elif optional == 2:
        plotter.plot_countries_with_most_appearances(amount)
    elif optional == 3:
        plotter.plot_countries_with_most_wins(amount)
    elif optional == 4:
        plotter.plot_countries_with_best_win_ratio(amount)
    else:
        raise ValueError


def country_menu(optional: int):
    country = input("Which country: ")
    interval = None
    if input("Do u want a specific interval?") != '':
        from_year = int(input("From year: "))
        to_year = int(input("To year: "))
        if to_year < from_year:
            raise ValueError
        interval = (from_year, to_year)
    if optional == 1:
        plotter.plot_country_goals_by_year(country, interval)
    elif optional == 2:
        plotter.plot_country_appearances_by_year(country, interval)
    elif optional == 3:
        plotter.plot_country_wins_by_year(country, interval)
    elif optional == 4:
        plotter.plot_country_win_ratio_by_year(country, interval)
    else:
        raise ValueError


if __name__ == '__main__':
    plotter = Plotter()
    while True:
        print("Select option:\n1 to display football statistics since 1872\n2 to display specific country statistics "
              "since 1872\n")
        input_char = input("> ")
        if input_char == '':
            exit(0)
        else:
            try:
                input_char = int(input_char)
                option = first_menu(input_char)
                if input_char == 1:
                    statistics_menu(option)
                elif input_char == 2:
                    country_menu(option)
                else:
                    raise ValueError
            except ValueError:
                print("Wrong option!")
