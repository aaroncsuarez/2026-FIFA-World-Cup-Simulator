import random
import math

TEAM_WIN_ODDS = {
    "Spain": 500,
    "France": 500,
    "England": 650,
    "Brazil": 800,
    "Argentina": 850,
    "Portugal": 1100,
    "Germany": 1400,
    "Netherlands": 2000,
    "Norway": 3000,
    "Belgium": 3500,
    "Colombia": 4000,
    "Morocco": 5000,
    "Japan": 5000,
    "United States": 6000,
    "Uruguay": 6500,
    "Mexico": 7500,
    "Switzerland": 8000,
    "Croatia": 8000,
    "Ecuador": 9000,
    "Türkiye": 10000,
    "Sweden": 10000,
    "Senegal": 11000,
    "Austria": 15000,
    "Paraguay": 15000,
    "Canada": 20000,
    "Scotland": 20000,
    "Czechia": 25000,
    "Ivory Coast": 25000,
    "Bosnia & Herzegovina": 25000,
    "Egypt": 30000,
    "Ghana": 30000,
    "Algeria": 35000,
    "South Korea": 45000,
    "Iran": 50000,
    "Australia": 50000,
    "Tunisia": 50000,
    "DR Congo": 70000,
    "South Africa": 80000,
    "Saudi Arabia": 100000,
    "Panama": 100000,
    "Qatar": 100000,
    "Uzbekistan": 100000,
    "New Zealand": 100000,
    "Iraq": 100000,
    "Cabo Verde": 100000,
    "Jordan": 200000,
    "Curaçao": 200000,
    "Haiti": 250000
}

def get_team_strength(team):
    odds = TEAM_WIN_ODDS.get(team["name"], 250000)

    #Convert odds into a usable strength scale
    #Lower odds = stronger team
    odds_strength = (100000 / odds) ** 0.85

    #Small FIFA ranking adjustment
    ranking_bonus = (101 - team["ranking"]) / 100
    strength = odds_strength * (0.85 + ranking_bonus * 0.15)

    return strength

def poisson_random(expected_goals):
    # Simple Poisson generator
    L = math.exp(-expected_goals)
    k = 0
    p = 1.0

    while p > L:
        k += 1
        p *= random.random()

    return k - 1


def simulate_regular_score(team1, team2):
    strength1 = get_team_strength(team1)
    strength2 = get_team_strength(team2)

    total_strength = strength1 + strength2

    # Modern World Cup average: around 2.6 total goals per match
    avg_total_goals = 2.35

    expected1 = avg_total_goals * (strength1 / total_strength)
    expected2 = avg_total_goals * (strength2 / total_strength)

    goals1 = poisson_random(expected1)
    goals2 = poisson_random(expected2)

    # Soft cap: prevents crazy scores most of the time
    goals1 = min(goals1, 5)
    goals2 = min(goals2, 5)

    return goals1, goals2


def simulate_group_match(team1, team2):
    goals1, goals2 = simulate_regular_score(team1, team2)

    return {
        "goals1": goals1,
        "goals2": goals2,
        "score": f"{goals1}-{goals2}"
    }


def simulate_extra_time_score(goals1, goals2, team1, team2):
    # Extra time usually has fewer goals
    strength1 = get_team_strength(team1)
    strength2 = get_team_strength(team2)

    total_strength = strength1 + strength2

    avg_extra_time_goals = 0.55

    expected1 = avg_extra_time_goals * (strength1 / total_strength)
    expected2 = avg_extra_time_goals * (strength2 / total_strength)

    extra1 = poisson_random(expected1)
    extra2 = poisson_random(expected2)

    return goals1 + extra1, goals2 + extra2


def simulate_penalty_shootout():
    shootout1 = 0
    shootout2 = 0

    shots1 = 0
    shots2 = 0

    success_rate = 0.71

    # First 5 penalties
    for round_number in range(5):
        shots1 += 1
        if random.random() < success_rate:
            shootout1 += 1

        remaining1 = 5 - shots1
        remaining2 = 5 - shots2

        if shootout1 > shootout2 + remaining2:
            return shootout1, shootout2

        shots2 += 1
        if random.random() < success_rate:
            shootout2 += 1

        remaining1 = 5 - shots1
        remaining2 = 5 - shots2

        if shootout2 > shootout1 + remaining1:
            return shootout1, shootout2

    # Sudden death
    while shootout1 == shootout2:
        team1_score = random.random() < success_rate
        team2_score = random.random() < success_rate

        if team1_score:
            shootout1 += 1
        if team2_score:
            shootout2 += 1

    return shootout1, shootout2


def simulate_knockout_match(team1, team2):
    goals1, goals2 = simulate_regular_score(team1, team2)

    if goals1 > goals2:
        return {
            "goals1": goals1,
            "goals2": goals2,
            "score": f"{goals1}-{goals2}",
            "result_type": "FT",
            "winner_side": 1
        }

    if goals2 > goals1:
        return {
            "goals1": goals1,
            "goals2": goals2,
            "score": f"{goals1}-{goals2}",
            "result_type": "FT",
            "winner_side": 2
        }

    aet1, aet2 = simulate_extra_time_score(goals1, goals2, team1, team2)

    if aet1 > aet2:
        return {
            "goals1": aet1,
            "goals2": aet2,
            "score": f"{aet1}-{aet2} (AET)",
            "result_type": "AET",
            "winner_side": 1
        }

    if aet2 > aet1:
        return {
            "goals1": aet1,
            "goals2": aet2,
            "score": f"{aet1}-{aet2} (AET)",
            "result_type": "AET",
            "winner_side": 2
        }

    pens1, pens2 = simulate_penalty_shootout()

    winner_side = 1 if pens1 > pens2 else 2

    return {
        "goals1": aet1,
        "goals2": aet2,
        "pens1": pens1,
        "pens2": pens2,
        "score": f"{aet1}-{aet2} ({pens1}-{pens2} P)",
        "result_type": "P",
        "winner_side": winner_side
    }