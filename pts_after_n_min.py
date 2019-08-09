# Given a number of minutes, calculates the number of points that team would receive if matches went up to that number of minutes.

from collections import defaultdict

def pts_after_n_min(n, fixtures):
    standings = defaultdict(int)
    for match in fixtures:
        scores = match['score_time']
        important_times = list(scores.keys())

        time = "NaN"
        for i in range(len(important_times)):
            if n < important_times[i]:
                time = important_times[i-1]
        if time == "NaN":
            time = important_times[-1]

        goal_diff = scores[time]


        if goal_diff > 0:
            #home team wins
            home_pts = 3
            away_pts = 0
        if goal_diff < 0:
            #away team wins
            home_pts = 0
            away_pts = 3    
        if goal_diff == 0:
            #draw
            home_pts, away_pts = (1,1)

        standings[match['home']] += home_pts
        standings[match['away']] += away_pts
    
    #for team in sorted(standings.items(), reverse=True, key=lambda x: x[1]):
    #    print(team[0] + ": " + str(team[1]))

    return standings