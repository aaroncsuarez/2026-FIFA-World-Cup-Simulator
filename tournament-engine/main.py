from engine.groups import (
    create_standings,
    record_match,
    print_group_table,
    get_group_qualifiers,
    get_best_third_place_teams,
    print_third_place_table,
    get_team_by_name
)

from engine.fixtures import GROUP_STAGE_MATCHES

from engine.simulator import simulate_group_match

from engine.bracket import (
    load_combinations,
    find_combination_row,
    build_round_of_32_schedule,
    print_round_of_32,
    ROUND_OF_16_TEMPLATE,
    build_next_round_schedule,
    QUARTER_FINAL_TEMPLATE,
    SEMI_FINAL_TEMPLATE,
    THIRD_PLACE_TEMPLATE,
    build_third_place_schedule,
    FINAL_TEMPLATE
)

from engine.knockout import predict_round, print_round_results

print("Tournament Mode")
print("1. Manual Tournament")
print("2. Simulate Entire Tournament")
print("3. Hybrid Mode")

TOURNAMENT_MODE = input("Choose 1, 2, or 3: ")

SIMULATE_REST_OF_GROUP_STAGE = False

def get_score(team_name):
    while True:
        try:
            score = int(input(f"Goals for {team_name}: "))
            if score < 0:
                print("Score cannot be negative.")
                continue
            return score
        except ValueError:
            print("Please enter a valid whole number.")

def choose_group_match_result(team1_name, team2_name):
    global SIMULATE_REST_OF_GROUP_STAGE

    if TOURNAMENT_MODE == "1":
        goals1 = get_score(team1_name)
        goals2 = get_score(team2_name)
        return goals1, goals2

    if TOURNAMENT_MODE == "2" or SIMULATE_REST_OF_GROUP_STAGE:
        team1 = get_team_by_name(team1_name)
        team2 = get_team_by_name(team2_name)

        result = simulate_group_match(team1, team2)

        print(f'Simulated Result: {team1_name} {result["score"]} {team2_name}')

        return result["goals1"], result["goals2"]

    if TOURNAMENT_MODE == "3":
        while True:
            print("\nChoose result option:")
            print("1. Enter score manually")
            print("2. Simulate match")
            print("3. Simulate remaining Group Stage matches")

            choice = input("Choose 1, 2, or 3: ")

            if choice == "1":
                goals1 = get_score(team1_name)
                goals2 = get_score(team2_name)
                return goals1, goals2

            if choice == "2":
                team1 = get_team_by_name(team1_name)
                team2 = get_team_by_name(team2_name)

                result = simulate_group_match(team1, team2)

                print(f'Simulated Result: {team1_name} {result["score"]} {team2_name}')

                return result["goals1"], result["goals2"]

            if choice == "3":
                SIMULATE_REST_OF_GROUP_STAGE = True

                team1 = get_team_by_name(team1_name)
                team2 = get_team_by_name(team2_name)

                result = simulate_group_match(team1, team2)

                print(f'Simulated Result: {team1_name} {result["score"]} {team2_name}')

                return result["goals1"], result["goals2"]

            print("Invalid choice.")

standings = create_standings()

for match in GROUP_STAGE_MATCHES:
    print(
        f'\nMatch #{match["match"]} - Group {match["group"]} '
        f'({match["date"]}, {match["location"]})'
    )

    print(f'{match["team1"]} vs {match["team2"]}')
    
    goals1, goals2 = choose_group_match_result(
        match["team1"],
        match["team2"]
    )

    record_match(
        standings,
        match["group"],
        match["team1"],
        match["team2"],
        goals1,
        goals2
    )

print("\nGROUP STAGE TABLES")

for group in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]:
    print_group_table(group, standings[group])

first, second, third = get_group_qualifiers(standings)
best_thirds = get_best_third_place_teams(third)

print_third_place_table(best_thirds)

best_third_groups = [team["group"] for team in best_thirds]

combinations = load_combinations("data/combinations.json")

row = find_combination_row(best_third_groups, combinations)

print("\nCombination Row Used:", row)

round_of_32_schedule = build_round_of_32_schedule(row, combinations)

print_round_of_32(round_of_32_schedule, first, second, third)

round_of_32_results = predict_round(round_of_32_schedule, TOURNAMENT_MODE, "Round of 32")

print_round_results(round_of_32_results, "Round of 32")

round_of_16_schedule = build_next_round_schedule(
    ROUND_OF_16_TEMPLATE,
    round_of_32_results
)

round_of_16_results = predict_round(round_of_16_schedule, TOURNAMENT_MODE, "Round of 16")

print_round_results(round_of_16_results, "Round of 16")

quarter_final_schedule = build_next_round_schedule(
    QUARTER_FINAL_TEMPLATE,
    round_of_16_results
)

quarter_final_results = predict_round(quarter_final_schedule, TOURNAMENT_MODE, "Quarter-Final")

print_round_results(quarter_final_results, "Quarter-Finals")


semi_final_schedule = build_next_round_schedule(
    SEMI_FINAL_TEMPLATE,
    quarter_final_results
)

semi_final_results = predict_round(semi_final_schedule, TOURNAMENT_MODE, "Semi-Finals")

print_round_results(semi_final_results, "Semi-Finals")

third_place_schedule = build_third_place_schedule(
    THIRD_PLACE_TEMPLATE,
    semi_final_results
)

third_place_results = predict_round(third_place_schedule, TOURNAMENT_MODE, "3rd Place Match")

print_round_results(third_place_results, "3rd Place Match")


final_schedule = build_next_round_schedule(
    FINAL_TEMPLATE,
    semi_final_results
)

final_results = predict_round(final_schedule, TOURNAMENT_MODE, "Final")

print_round_results(final_results, "Final")

champion = final_results[104]["winner"]
runner_up = final_results[104]["runner_up"]
third_place = third_place_results[103]["winner"]

print("Winner 🏆")
print(champion)

print("\nTop 3")
print(f"🥇 {champion}")
print(f"🥈 {runner_up}")
print(f"🥉 {third_place}")
