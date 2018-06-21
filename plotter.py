import pandas as pd
import matplotlib.pyplot as plt
import operator


class Plotter:

    def __init__(self):
        self.matches = pd.read_csv("data/results.csv")
        self.matches.replace({'Germany DR': 'Germany', 'China': 'China PR'})
        self.matches['date'] = pd.to_datetime(self.matches['date'])
        self.get_results()

    def get_results(self):
        results = []
        for _, row in self.matches.iterrows():
            if row['home_score'] > row['away_score']:
                results.append(row['home_team'])
            elif row['away_score'] > row['home_score']:
                results.append(row['away_team'])
            else:
                results.append('Draw')
        self.matches['result'] = results

    def get_goals_amount(self, country: str):
        goals = 0
        for _, row in self.matches.iterrows():
            if row['home_team'] == country:
                goals += row['home_score']
            elif row['away_team'] == country:
                goals += row['away_score']
        return goals

    def get_appearances(self, country: str):
        appearances = 0
        for _, row in self.matches.iterrows():
            if row['home_team'] == country or row['away_team'] == country:
                appearances += 1
        return appearances

    def get_wins(self, country: str):
        wins = 0
        for _, row in self.matches.iterrows():
            if row['result'] == country:
                wins += 1
        return wins

    def get_countries_with_appearances(self, n=None):
        countries = {}
        for _, row in self.matches.iterrows():
            if row['home_team'] not in countries:
                countries[row['home_team']] = 1
            else:
                countries[row['home_team']] += 1
            if row['away_team'] not in countries:
                countries[row['away_team']] = 1
            else:
                countries[row['away_team']] += 1
        countries = sorted(countries.items(), key=operator.itemgetter(1), reverse=True)
        if n is None:
            return countries
        else:
            return Plotter.take(n, countries)

    def get_countries_with_goals(self, n=None):
        countries = {}
        for _, row in self.matches.iterrows():
            if row['home_team'] not in countries:
                countries[row['home_team']] = row['home_score']
            else:
                countries[row['home_team']] += row['home_score']
            if row['away_team'] not in countries:
                countries[row['away_team']] = row['away_score']
            else:
                countries[row['away_team']] += row['away_score']
        countries = sorted(countries.items(), key=operator.itemgetter(1), reverse=True)
        if n is None:
            return countries
        else:
            return Plotter.take(n, countries)

    def get_countries_with_most_wins(self, n=None):
        countries = {}
        for _, row in self.matches.iterrows():
            if row['result'] != 'Draw':
                if row['result'] not in countries:
                    countries[row['result']] = 1
                else:
                    countries[row['result']] += 1
        countries = sorted(countries.items(), key=operator.itemgetter(1), reverse=True)
        if n is None:
            return countries
        else:
            return Plotter.take(n, countries)

    def get_country_goals_by_year(self, country: str):
        years = {}
        for _, row in self.matches.iterrows():
            if row['home_team'] == country:
                if row['date'].year in years:
                    years[row['date'].year] += row['home_score']
                else:
                    years[row['date'].year] = row['home_score']
            if row['away_team'] == country:
                if row['date'].year in years:
                    years[row['date'].year] += row['away_score']
                else:
                    years[row['date'].year] = row['away_score']
        return sorted(years.items(), key=operator.itemgetter(0))

    def get_country_appearances_by_year(self, country: str):
        years = {}
        for _, row in self.matches.iterrows():
            if row['home_team'] == country:
                if row['date'].year in years:
                    years[row['date'].year] += 1
                else:
                    years[row['date'].year] = 1
            if row['away_team'] == country:
                if row['date'].year in years:
                    years[row['date'].year] += 1
                else:
                    years[row['date'].year] = 1
        return sorted(years.items(), key=operator.itemgetter(0))

    def get_country_by_win_ratio(self):
        wins = self.get_countries_with_most_wins()
        appearances = dict(self.get_countries_with_appearances())
        win_ratio = {}
        for i, v in wins:
            win_ratio[i] = v / appearances[i]
        return sorted(win_ratio.items(), key=operator.itemgetter(1), reverse=True)

    def get_country_win_ratio_by_year(self, country: str):
        wins = self.get_country_wins_by_year(country)
        appearances = dict(self.get_country_appearances_by_year(country))
        win_ratio = {}
        for i, v in wins:
            win_ratio[i] = v / appearances[i]
        return sorted(win_ratio.items(), key=operator.itemgetter(0))

    def get_country_wins_by_year(self, country: str):
        years = {}
        for _, row in self.matches.iterrows():
            if row['result'] == country:
                if row['date'].year in years:
                    years[row['date'].year] += 1
                else:
                    years[row['date'].year] = 1
        return sorted(years.items(), key=operator.itemgetter(0))

    def plot_countries_with_most_appearances(self, n: int):
        data = self.get_countries_with_appearances(n)
        countries = [i[0] for i in data]
        appearances = [i[1] for i in data]
        plt.barh(countries, appearances)
        plt.title("Top {} countries with respect to appearances".format(n))
        for a, b in zip(countries, appearances):
            plt.text(b, a, str(b))
        plt.xlabel("Appearances", fontsize=13)
        plt.show()

    def plot_countries_with_most_wins(self, n: int):
        data = self.get_countries_with_most_wins(n)
        countries = [i[0] for i in data]
        wins = [i[1] for i in data]
        plt.barh(countries, wins)
        plt.title("Top {} countries with respect to wins".format(n))
        for a, b in zip(countries, wins):
            plt.text(b, a, str(b))
        plt.xlabel("Wins", fontsize=13)
        plt.show()

    def plot_countries_with_best_win_ratio(self, n: int):
        data = Plotter.take(n, self.get_country_by_win_ratio())
        countries = [i[0] for i in data]
        wins = [i[1] for i in data]
        plt.barh(countries, wins)
        plt.title("Top {} countries by win-ratio".format(n))
        plt.xlabel("Win-ratio", fontsize=13)
        for a, b in zip(countries, wins):
            plt.text(b, a, "%.2f" % b)
        plt.show()

    def plot_countries_with_most_goals(self, n: int):
        data = self.get_countries_with_goals(n)
        countries = [i[0] for i in data]
        goals = [i[1] for i in data]
        plt.barh(countries, goals)
        plt.title("Top {} countries with respect to goals scored".format(n))
        plt.xlabel("Goals", fontsize=13)
        for a, b in zip(countries, goals):
            plt.text(b, a, str(b))
        plt.show()

    def plot_country_win_ratio_by_year(self, country: str, interval=None):
        win_ratios = self.get_country_win_ratio_by_year(country)
        if interval is not None:
            win_ratios = list(filter(lambda x: interval[0] <= x[0] <= interval[1], win_ratios))
        years = [i[0] for i in win_ratios]
        win_rate = [i[1] for i in win_ratios]
        plt.bar(years, win_rate)
        if interval is None:
            plt.title("Win-ratio of {} each year".format(country))
        else:
            plt.title("Win-ratio of {} since {} to {}".format(country, interval[0], interval[1]))
        plt.xticks(rotation='vertical')
        plt.ylabel("Win-ratio", fontsize=13, rotation='vertical')
        plt.show()

    def plot_country_goals_by_year(self, country: str, interval=None):
        results = self.get_country_goals_by_year(country)
        if interval is not None:
            results = list(filter(lambda x: interval[0] <= x[0] <= interval[1], results))
        years = [i[0] for i in results]
        goals = [i[1] for i in results]
        plt.bar(years, goals)
        if interval is None:
            plt.title("Goals scored by {} each year".format(country))
        else:
            plt.title("Goals scored by {} from {} to {}".format(country, interval[0], interval[1]))
        plt.xticks(rotation='vertical')
        plt.ylabel("Goals", fontsize=13, rotation='vertical')
        plt.show()

    def plot_country_appearances_by_year(self, country: str, interval=None):
        results = self.get_country_appearances_by_year(country)
        if interval is not None:
            results = list(filter(lambda x: interval[0] <= x[0] <= interval[1], results))
        years = [i[0] for i in results]
        appearances = [i[1] for i in results]
        plt.bar(years, appearances)
        if interval is None:
            plt.title("Appearances of {} each year".format(country))
        else:
            plt.title("Appearances of {} from {} to {}".format(country, interval[0], interval[1]))
        plt.xticks(rotation='vertical')
        plt.ylabel("Appearances", fontsize=13, rotation='vertical')
        plt.show()

    def plot_country_wins_by_year(self, country: str, interval=None):
        results = self.get_country_wins_by_year(country)
        if interval is not None:
            results = list(filter(lambda x: interval[0] <= x[0] <= interval[1], results))
        years = [i[0] for i in results]
        wins = [i[1] for i in results]
        plt.bar(years, wins)
        if interval is None:
            plt.title("Wins of {} each year".format(country))
        else:
            plt.title("Wins of {} from {} to {}".format(country, interval[0], interval[1]))
        plt.xticks(rotation='vertical')
        plt.ylabel("Wins", fontsize=13, rotation='vertical')
        plt.show()

    @staticmethod
    def take(n: int, iterable):
        from itertools import islice
        return list(islice(iterable, n))
