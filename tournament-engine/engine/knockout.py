from engine.groups import get_team_by_name
from engine.simulator import simulate_knockout_match

def get_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Score cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")

def predict_knockout_match(match, tournament_mode, round_name, simulate_rest_of_round=False):
    team1 = match["team1_name"]
    team2 = match["team2_name"]

    print(f'\nMatch #{match["match"]} - {team1} vs {team2}')
    print(f'Location: {match["location"]}')

    if tournament_mode == "1":
        return enter_knockout_result_manually(match)

    if tournament_mode == "2" or simulate_rest_of_round:
        return simulate_knockout_result(match)

    if tournament_mode == "3":
        while True:
            print("\nChoose result option:")
            print("1. Enter score manually")
            print("2. Simulate match")
            print(f"3. Simulate remaining {round_name} matches")

            choice = input("Choose 1, 2, or 3: ")

            if choice == "1":
                return enter_knockout_result_manually(match)

            if choice == "2":
                return simulate_knockout_result(match)

            if choice == "3":
                result = simulate_knockout_result(match)
                result["simulate_rest_of_round"] = True
                return result

            print("Invalid choice.")

def simulate_knockout_result(match):
    team1 = match["team1_name"]
    team2 = match["team2_name"]

    team1_data = get_team_by_name(team1)
    team2_data = get_team_by_name(team2)

    result = simulate_knockout_match(team1_data, team2_data)

    winner = team1 if result["winner_side"] == 1 else team2
    runner_up = team2 if winner == team1 else team1

    print(f'Simulated Result: {team1} {result["score"]} {team2}')

    return {
        **match,
        "score": result["score"],
        "result_type": result["result_type"],
        "winner": winner,
        "runner_up": runner_up
    }


def enter_knockout_result_manually(match):
    team1 = match["team1_name"]
    team2 = match["team2_name"]

    while True:
        print("\nResult type:")
        print("1. Full Time")
        print("2. After Extra Time")
        print("3. Penalties")

        choice = input("Choose 1, 2, or 3: ")

        if choice not in ["1", "2", "3"]:
            print("Invalid choice.")
            continue

        goals1 = get_int(f"{team1} goals: ")
        goals2 = get_int(f"{team2} goals: ")

        if choice == "1":
            if goals1 == goals2:
                print("Knockout matches cannot end tied at full time.")
                continue

            winner = team1 if goals1 > goals2 else team2
            return {
                **match,
                "score": f"{goals1}-{goals2}",
                "result_type": "FT",
                "winner": winner,
                "runner_up": team2 if winner == team1 else team1
            }

        if choice == "2":
            if goals1 == goals2:
                print("AET score must have a winner unless going to penalties.")
                continue

            winner = team1 if goals1 > goals2 else team2
            return {
                **match,
                "score": f"{goals1}-{goals2} (AET)",
                "result_type": "AET",
                "winner": winner,
                "runner_up": team2 if winner == team1 else team1
            }

        if choice == "3":
            if goals1 != goals2:
                print("Penalty matches should be tied after extra time.")
                continue

            pens1 = get_int(f"{team1} penalty goals: ")
            pens2 = get_int(f"{team2} penalty goals: ")

            if pens1 == pens2:
                print("Penalty shootout cannot end tied.")
                continue

            winner = team1 if pens1 > pens2 else team2
            return {
                **match,
                "score": f"{goals1}-{goals2} ({pens1}-{pens2} P)",
                "result_type": "P",
                "winner": winner,
                "runner_up": team2 if winner == team1 else team1
            }


def predict_round(matches, tournament_mode, round_name):
    results = {}
    simulate_rest_of_round = False

    for match in matches:
        result = predict_knockout_match(
            match,
            tournament_mode,
            round_name,
            simulate_rest_of_round
        )

        if result.get("simulate_rest_of_round"):
            simulate_rest_of_round = True

        results[result["match"]] = result

    return results


def print_round_results(results, round_name):
    print(f"\n{round_name} Results:\n")

    for match_number in sorted(results):
        result = results[match_number]

        print(
            f'{result["team1_name"]} {result["score"]} {result["team2_name"]} '
            f'(Match #{result["match"]} {result["location"]})'
        )
        print(f'Winner: {result["winner"]}\n')