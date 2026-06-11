import json

FIXED_SLOTS = [
    "1A", "1B", "1D", "1E",
    "1G", "1I", "1K", "1L"
]

THIRD_PLACE_MATCH_NUMBERS = {
    "1A": 79,
    "1B": 85,
    "1D": 81,
    "1E": 74,
    "1G": 82,
    "1I": 77,
    "1K": 87,
    "1L": 80,
}

ROUND_OF_32_TEMPLATE = [
    {"match": 73, "date": "June 28", "location": "Los Angeles", "team1": "2A", "team2": "2B"},
    {"match": 76, "date": "June 29", "location": "Houston", "team1": "1C", "team2": "2F"},
    {"match": 74, "date": "June 29", "location": "Boston", "team1": "1E", "team2": None},
    {"match": 75, "date": "June 29", "location": "Monterrey", "team1": "1F", "team2": "2C"},
    {"match": 78, "date": "June 30", "location": "Dallas", "team1": "2E", "team2": "2I"},
    {"match": 77, "date": "June 30", "location": "New York", "team1": "1I", "team2": None},
    {"match": 79, "date": "June 30", "location": "Mexico City", "team1": "1A", "team2": None},
    {"match": 80, "date": "July 1", "location": "Atlanta", "team1": "1L", "team2": None},
    {"match": 82, "date": "July 1", "location": "Seattle", "team1": "1G", "team2": None},
    {"match": 81, "date": "July 1", "location": "San Francisco", "team1": "1D", "team2": None},
    {"match": 84, "date": "July 2", "location": "Los Angeles", "team1": "1H", "team2": "2J"},
    {"match": 83, "date": "July 2", "location": "Toronto", "team1": "2K", "team2": "2L"},
    {"match": 85, "date": "July 2", "location": "Vancouver", "team1": "1B", "team2": None},
    {"match": 88, "date": "July 3", "location": "Dallas", "team1": "2D", "team2": "2G"},
    {"match": 86, "date": "July 3", "location": "Miami", "team1": "1J", "team2": "2H"},
    {"match": 87, "date": "July 3", "location": "Kansas City", "team1": "1K", "team2": None},
]

ROUND_OF_16_TEMPLATE = [
    {"match": 90, "date": "July 4", "location": "Houston", "team1_from": 73, "team2_from": 75},
    {"match": 89, "date": "July 4", "location": "Philadelphia", "team1_from": 74, "team2_from": 77},
    {"match": 91, "date": "July 5", "location": "New York", "team1_from": 76, "team2_from": 78},
    {"match": 92, "date": "July 5", "location": "Mexico City", "team1_from": 79, "team2_from": 80},
    {"match": 93, "date": "July 6", "location": "Dallas", "team1_from": 83, "team2_from": 84},
    {"match": 94, "date": "July 6", "location": "Seattle", "team1_from": 81, "team2_from": 82},
    {"match": 95, "date": "July 7", "location": "Atlanta", "team1_from": 86, "team2_from": 88},
    {"match": 96, "date": "July 7", "location": "Vancouver", "team1_from": 85, "team2_from": 87}
]

QUARTER_FINAL_TEMPLATE = [
     {"match": 97, "date": "July 9", "location": "Boston", "team1_from": 89, "team2_from": 90},
     {"match": 98, "date": "July 10", "location": "Los Angeles", "team1_from": 93, "team2_from": 94},
     {"match": 99, "date": "July 11", "location": "Miami", "team1_from": 91, "team2_from": 92},
     {"match": 100, "date": "July 11", "location": "Kansas City", "team1_from": 95, "team2_from": 96}
]

SEMI_FINAL_TEMPLATE = [
     {"match": 101, "date": "July 14", "location": "Dallas", "team1_from": 97, "team2_from": 98},
     {"match": 102, "date": "July 15", "location": "Atlanta", "team1_from": 99, "team2_from": 100}
]

THIRD_PLACE_TEMPLATE = [
     {"match": 103, "date": "July 18", "location": "Miami", "team1_from": 101, "team2_from": 102}
]

FINAL_TEMPLATE = [
     {"match": 104, "date": "July 19", "location": "New York", "team1_from": 101, "team2_from": 102}
]


def load_combinations(path):
    with open(path, "r") as f:
        return json.load(f)
    
def find_combination_row(groups, combinations):
    target = set(groups)

    for row, third_place_slots in combinations.items():
        row_groups = set(item[-1] for item in third_place_slots)

        if row_groups == target:
            return row
        
    return None

def build_dynamic_third_place_matchups(row, combinations):
    if row not in combinations:
        raise ValueError(f"No combination found for row: {row}")
    
    third_place_slots = combinations[row]
    dynamic_matchups = {}

    for fixed_team, third_place_team in zip(FIXED_SLOTS, third_place_slots):
        match_number = THIRD_PLACE_MATCH_NUMBERS[fixed_team]
        dynamic_matchups[match_number] = third_place_team

    return dynamic_matchups
    
def build_round_of_32_schedule(row, combinations):
        dynamic_matchups = build_dynamic_third_place_matchups(row, combinations)

        schedule = []

        for match in ROUND_OF_32_TEMPLATE:
            completed_match = match.copy()

            if completed_match["team2"] is None:
                completed_match["team2"] = dynamic_matchups[completed_match["match"]]

            schedule.append(completed_match)

        return schedule

def build_next_round_schedule(template, previous_results):
    schedule = []

    for match in template:
        team1 = previous_results[match["team1_from"]]["winner"]
        team2 = previous_results[match["team2_from"]]["winner"]

        schedule.append({
            "match": match["match"],
            "date": match["date"],
            "location": match["location"],
            "team1_name": team1,
            "team2_name": team2
        })

    return schedule

def build_third_place_schedule(template, semi_final_results):
    schedule = []

    for match in template:
        team1 = semi_final_results[match["team1_from"]]["runner_up"]
        team2 = semi_final_results[match["team2_from"]]["runner_up"]

        schedule.append({
            "match": match["match"],
            "date": match["date"],
            "location": match["location"],
            "team1_name": team1,
            "team2_name": team2
        })

    return schedule

def resolve_seed(seed, first, second, third):
     place = seed[0]
     group = seed[1]

     if place == "1":
          return first[group]["team"]
     elif place == "2":
          return second[group]["team"]
     elif place == "3":
          return third[group]["team"]
    
def print_round_of_32(schedule, first, second, third):
        print("\nRound of 32 Schedule:\n")

        current_date = ""

        for match in schedule:
            if match["date"] != current_date:
                current_date = match["date"]
                print(current_date)

            team1 = resolve_seed(match["team1"], first, second, third)
            team2 = resolve_seed(match["team2"], first, second, third)
            
            match["team1_name"] = team1
            match["team2_name"] = team2

            print(
                f'{team1} vs {team2} '
                f'(Match #{match["match"]} {match["location"]})'
            )

