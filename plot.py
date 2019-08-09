# Visualises points by minutes

from pts_after_n_min import pts_after_n_min as panm
from collections import defaultdict
import matplotlib.pyplot as plt

def plot_results(fixtures):
    teams = defaultdict(list)

    for i in range(1, 91):
        results = panm(i, fixtures)
        #print(results)

        for team in results:
            teams[team].append(results[team])
    
    for team in sorted(teams.items(), reverse=True, key=lambda x: x[1]):
        minutes = [i for i in range(1, 91)]
        plt.plot(minutes, team[1], label=team[0])
        plt.legend(loc='upper left')
    plt.show()