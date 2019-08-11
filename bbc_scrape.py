# Scrapes data from the BBC sport website

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import re

from datetime import datetime
from dateutil.relativedelta import relativedelta


def months_thru(start_month, end_month):
    #given two months in the form YYYY-MM, gives all months between the two months inclusive.
    
    startDate = start_month + '-01'
    endDate = end_month + '-01'

    cur_date = start = datetime.strptime(startDate, '%Y-%m-%d').date()
    end = datetime.strptime(endDate, '%Y-%m-%d').date()

    months = []

    while cur_date < end:
        months.append(str(cur_date)[:7])
        cur_date += relativedelta(months=1)

    months.append(end_month)
    print(months)
    return(months)

def parse(start_month, end_month):

    months = months_thru(start_month, end_month)
    fixture_summary = []
    driver = webdriver.Chrome()
    for month in months:
        url = f"https://www.bbc.co.uk/sport/football/scottish-premiership/scores-fixtures/{month}?filter=results" #start with august results only...

        
        driver.get(url)

        driver.find_elements_by_xpath("//*[contains(text(), 'Show scorers')]")[0].click()
        sleep(3)
        print("awake")
        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")
        matches = soup.findAll("article", {"class": "sp-c-fixture"})
        print("found matches...")
        print(len(matches))


        for match in matches:
            teams = match.findAll("span", {"class": "gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc"})

            home_team = teams[0].text
            away_team = teams[1].text
            
            home_info = match.findAll("ul", {"class": "sp-c-fixture__scorers sp-c-fixture__scorers-home gel-brevier"})
            away_info = match.findAll("ul", {"class": "sp-c-fixture__scorers sp-c-fixture__scorers-away gel-brevier"})

            def get_scorers(team_info):
                team_text = ""
                for info in team_info:
                    lis = info.findAll("li")
                    for li in lis:
                        team_text += li.text
                
                print(team_text)


                scorers = re.findall(r'\(([^)]+)', team_text)

                def clean_text(goal):

                    goals_by_scorer = []
                    all_goals = goal.split(", ")
                    for ag in all_goals:
                        if "D" not in ag:
                            gt_text = ag.split()[0]
                            print(gt_text)
                            if "+" in gt_text:
                                added_time = gt_text.split('+')[1]
                                goals_by_scorer.append(90 + int(added_time))
                            else:
                                goals_by_scorer.append(int(gt_text[:-1]))
                    
                    return goals_by_scorer
                    
                    
                
                scorers = [clean_text(s) for s in scorers]

                if scorers is not None:
                    scorers = [y for x in scorers for y in x]
            
                return(scorers)


            home_scorers = get_scorers(home_info)
            away_scorers = get_scorers(away_info)

            current_score = 0
            score_time = {0: 0}

            def minm(a):
                # get the minimum value of an array, or +ve infinity if it's empty.
                if not a:
                    return float("inf")
                return min(a)

            while home_scorers or away_scorers:
                min_h, min_a = minm(home_scorers), minm(away_scorers)

                if min_a < min_h:
                    current_score -= 1
                    score_time[min_a] = current_score
                    away_scorers.remove(min_a)
                else:
                    current_score += 1
                    score_time[min_h] = current_score
                    home_scorers.remove(min_h)

            
            fixture = {'home': home_team,
                    'away': away_team,
                    'score_time': score_time}
            fixture_summary.append(fixture)
        print(month + "IS DONE")

    print(len(fixture_summary)) #this should be 186!!!
    return(fixture_summary)
