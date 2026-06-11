GROUPS = {
    "A": [
        {"name": "Mexico", "ranking": 15},
        {"name": "South Africa", "ranking": 60},
        {"name": "South Korea", "ranking": 25},
        {"name": "Czechia", "ranking": 41}
    ],
    "B": [
        {"name": "Canada", "ranking": 30},
        {"name": "Bosnia & Herzegovina", "ranking": 65},
        {"name": "Qatar", "ranking": 55},
        {"name": "Switzerland", "ranking": 19}
    ],
    "C": [
        {"name": "Brazil", "ranking": 6},
        {"name": "Morocco", "ranking": 8},
        {"name": "Haiti", "ranking": 83},
        {"name": "Scotland", "ranking": 43}
    ],
    "D": [
        {"name": "United States", "ranking": 16},
        {"name": "Paraguay", "ranking": 40},
        {"name": "Australia", "ranking": 27},
        {"name": "Türkiye", "ranking": 22}
    ],
    "E": [
        {"name": "Germany", "ranking": 10},
        {"name": "Curaçao", "ranking": 82},
        {"name": "Ivory Coast", "ranking": 34},
        {"name": "Ecuador", "ranking": 23}
    ],
    "F": [
        {"name": "Netherlands", "ranking": 7},
        {"name": "Japan", "ranking": 18},
        {"name": "Sweden", "ranking": 38},
        {"name": "Tunisia", "ranking": 44}
    ],
    "G": [
        {"name": "Belgium", "ranking": 9},
        {"name": "Egypt", "ranking": 29},
        {"name": "Iran", "ranking": 21},
        {"name": "New Zealand", "ranking": 85}
    ],
    "H": [
        {"name": "Spain", "ranking": 2},
        {"name": "Cabo Verde", "ranking": 69},
        {"name": "Saudi Arabia", "ranking": 61},
        {"name": "Uruguay", "ranking": 17}
    ],
    "I": [
        {"name": "France", "ranking": 1},
        {"name": "Senegal", "ranking": 14},
        {"name": "Iraq", "ranking": 57},
        {"name": "Norway", "ranking": 31}
    ],
    "J": [
        {"name": "Argentina", "ranking": 3},
        {"name": "Algeria", "ranking": 28},
        {"name": "Austria", "ranking": 24},
        {"name": "Jordan", "ranking": 63}
    ],
    "K": [
        {"name": "Portugal", "ranking": 5},
        {"name": "DR Congo", "ranking": 46},
        {"name": "Uzbekistan", "ranking": 50},
        {"name": "Colombia", "ranking": 13}
    ],
    "L": [
        {"name": "England", "ranking": 4},
        {"name": "Croatia", "ranking": 11},
        {"name": "Ghana", "ranking": 74},
        {"name": "Panama", "ranking": 33}
    ],
}

def create_standings():
    standings = {}

    for group_letter, teams in GROUPS.items():
        standings[group_letter] = []

        for team in teams:
            standings[group_letter].append({
                "team": team["name"],
                "ranking": team["ranking"],
                "group": group_letter,
                "MP": 0,
                "W": 0,
                "D": 0,
                "L": 0,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "PTS": 0,
            })

    return standings

def record_match(standings, group, team1_name, team2_name, goals1, goals2):
    team1 = find_team(standings[group], team1_name)
    team2 = find_team(standings[group], team2_name)

    team1["MP"] += 1
    team2["MP"] += 1

    team1["GF"] += goals1
    team1["GA"] += goals2

    team2["GF"] += goals2
    team2["GA"] += goals1

    team1["GD"] = team1["GF"] - team1["GA"]
    team2["GD"] = team2["GF"] - team2["GA"]

    if goals1 > goals2:
        team1["W"] += 1
        team2["L"] += 1
        team1["PTS"] += 3
    elif goals2 > goals1:
        team2["W"] += 1
        team1["L"] += 1
        team2["PTS"] += 3
    else:
        team1["D"] += 1
        team2["D"] += 1
        team1["PTS"] += 1
        team2["PTS"] += 1

def find_team(group_table, team_name):
    for team in group_table:
        if team["team"] == team_name:
            return team
        
    raise ValueError(f"Team not found: {team_name}")

def sort_group(group_table):
    return sorted(
        group_table,
        key=lambda team: (
            team["PTS"],
            team["GD"],
            team["GF"],
            -team["ranking"]
        ),
        reverse=True
    )

def print_group_table(group, group_table):
    sorted_table = sort_group(group_table)

    row_format = "{:<35} {:>2} {:>2} {:>2} {:>2} {:>3} {:>3} {:>3} {:>4}"

    print(f"\nGroup {group}")
    print(row_format.format("Team", "MP", "W", "D", "L", "GF", "GA", "GD", "  PTS"))

    for team in sorted_table:
        print(row_format.format(
            team["team"],
            team["MP"],
            team["W"],
            team["D"],
            team["L"],
            team["GF"],
            team["GA"],
            team["GD"],
            team["PTS"]
        ))

def get_group_qualifiers(standings):
    first_place = {}
    second_place = {}
    third_place = {}

    for group, table in standings.items():
        sorted_table = sort_group(table)

        first_place[group] = sorted_table[0]
        second_place[group] = sorted_table[1]
        third_place[group] = sorted_table[2]

    return first_place, second_place, third_place

def get_best_third_place_teams(third_place):
    teams = list(third_place.values())

    sorted_thirds = sorted(
        teams,
        key=lambda team: (
            team["PTS"],
            team["GD"],
            team["GF"],
            -team["ranking"]
        ),
        reverse=True
    )

    return sorted_thirds[:8]

def print_third_place_table(best_thirds):
    row_format = "{:<35} {:>2} {:>2} {:>2} {:>2} {:>3} {:>3} {:>3} {:>4} {:>5}"

    print("\nBest 3rd Place Teams")
    print(row_format.format("Team", "MP", "W", "D", "L", "GF", "GA", "GD", "  PTS", " Group"))

    for team in best_thirds:
        print(row_format.format(
            team["team"],
            team["MP"],
            team["W"],
            team["D"],
            team["L"],
            team["GF"],
            team["GA"],
            team["GD"],
            team["PTS"],
            team["group"]
        ))

def get_team_by_name(team_name):
    for group_teams in GROUPS.values():
        for team in group_teams:
            if team["name"] == team_name:
                return team
            
    raise ValueError(f"Team not found: {team_name}")