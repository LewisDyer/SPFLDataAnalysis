#This script gets data from soccerbot (in the folder), and produces a list of fixtures, showing the teams involved, and the score at various points in the game

#UPDATE (11/08/19) - Due to being outdated, I'm stopping work on the soccerbot scraper, and shifting towards a BBC Sport scraper.

import re
from bs4 import BeautifulSoup

def parse(filename):
    soup = BeautifulSoup(open(filename), "html.parser")

    for e in soup.findAll('br'):
        e.replace_with('***')

    fixture_table = soup.findAll("table")[0]

    fixtures = fixture_table.findAll("tr")[1:]

    fixture_summary = []

    for fixture in fixtures:
        fixture_info = fixture.findAll("b")
        goalscorers = fixture.findAll("div", {"class":"sbscorers"})

        
        while(len(goalscorers) < 2):
            goalscorers.append(BeautifulSoup("<div></div>", "html.parser"))

        gh = str(goalscorers[0]) or "none"
        ga = str(goalscorers[1]) or "none"
    
        g_home = re.findall(r'\(([^)]+)', gh)
        g_away = re.findall(r'\(([^)]+)', ga)

        def goal_sort(gt):
            return int(gt[:-1])

        g_times = []
        for scorer in g_home:
            temp = [ch for ch in scorer.split(',')]
            for time in temp:
                new_time = re.sub("[^0-9]", "", time)
                g_times.append(new_time + "+")
        a_times = []
        for scorer in g_away:
            temp = [ch for ch in scorer.split(',')]
            for time in temp:
                new_time = re.sub("[^0-9]", "", time)
                g_times.append(new_time + "-")        
        g_times = sorted(g_times, key=goal_sort)

        cum_score = {0:0}
        score = 0

        for goal in g_times:
            if goal[-1] == "+":
                score += 1
            else:
                score -= 1
            cum_score[goal_sort(goal)] = score       
        score_diff = int(fixture_info[1].string) - int(fixture_info[2].string)
        if score_diff != score:
            # in this case, the home team didn't score any goals.
            # negate all values in cum_score
            cum_score = {key:-cum_score[key] for key in cum_score}

        fixture_dict = {"home": fixture_info[0].string,
                        "away": fixture_info[3].string,
                        "score_time": cum_score}
        fixture_summary.append(fixture_dict)
    print(fixture_summary)
    return fixture_summary

parse("spd13.html")
