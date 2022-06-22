from copy import deepcopy
def test_challenge1():
    from challenge1 import MEASUREMENTS, get_number_of_increasing_measurements,get_number_of_increasing_sliding_windows
    assert get_number_of_increasing_measurements(MEASUREMENTS) == 1791
    assert get_number_of_increasing_sliding_windows(MEASUREMENTS) == 1822

def test_challenge2():
    from challenge2 import MOVES, get_position_value, get_improved_position_value
    assert get_position_value(MOVES) == 1451208
    assert get_improved_position_value(MOVES) == 1620141160

def test_challenge3():
    from challenge3 import NUMBERS, get_power_rate, get_life_support_rating
    assert get_power_rate(NUMBERS) == 3320834
    assert get_life_support_rating(NUMBERS) == 4481199

def test_challenge4():
    from challenge4 import GAME, get_winning_board_score, get_losing_board_score
    assert get_winning_board_score(GAME) == 51776
    assert get_losing_board_score(GAME) == 16830

def test_challenge5():
    from challenge5 import LINES, get_number_of_overlapping_points, get_number_of_overlapping_points_no_diagonal
    assert get_number_of_overlapping_points_no_diagonal(LINES) == 5147
    assert get_number_of_overlapping_points(LINES) == 16925

def test_challenge6():
    from challenge6 import LANTERNFISH, get_lanternfish_after
    assert get_lanternfish_after(LANTERNFISH, days=80) == 360761
    assert get_lanternfish_after(LANTERNFISH, days=256) == 1632779838045

def test_challenge7():
    from challenge7 import CRABS, get_fuel_spent
    assert get_fuel_spent(CRABS) == 336721
    assert get_fuel_spent(CRABS, True) == 91638945

def test_challenge8():
    from challenge8 import DIGIT_DISPLAYS, get_number_of_easy_numbers, get_decoded_sum
    assert get_number_of_easy_numbers(DIGIT_DISPLAYS) == 288
    assert get_decoded_sum(DIGIT_DISPLAYS) == 940724

def test_challenge9():
    from challenge9 import GRID, get_total_risk_level, get_largest_basins_product
    assert get_total_risk_level(GRID) == 550
    assert get_largest_basins_product(GRID) == 1100682

def test_challenge10():
    from challenge10 import LINES, get_corrupted_score, get_incomplete_score
    assert get_corrupted_score(LINES) == 271245
    assert get_incomplete_score(LINES) == 1685293086

def test_challenge11():
    from challenge11 import OCTOPODES, get_number_of_flashes, get_synchronization
    assert get_number_of_flashes(deepcopy(OCTOPODES)) == 1667
    assert get_synchronization(OCTOPODES) == 488

def test_challenge12():
    from challenge12 import PATHS, get_number_of_distinct_paths, get_number_of_modified_paths
    assert get_number_of_distinct_paths(PATHS) == 3802
    assert get_number_of_modified_paths(PATHS) == 99448

def test_challenge13():
    from challenge13 import INSTRUCTIONS, get_visible_points_after_first_fold
    assert get_visible_points_after_first_fold(INSTRUCTIONS) == 693

def test_challenge14():
    from challenge14 import POLYMERS, get_difference_of_most_and_least_common
    assert get_difference_of_most_and_least_common(POLYMERS) == 3408
    assert get_difference_of_most_and_least_common(POLYMERS, times=40) == 3724343376942

def test_challenge15():
    from challenge15 import GRID, get_lowest_risk, get_lowest_risk_big_grid
    assert get_lowest_risk(GRID) == 811
    assert get_lowest_risk_big_grid(GRID) == 3012

def test_challenge16():
    from challenge16 import PACKET, get_version_numbers
    assert get_version_numbers(PACKET) == 955
    assert PACKET.get_value() == 158135423448

def test_challenge17():
    from challenge17 import TARGET, get_highest_y, get_total_number_of_shots
    assert get_highest_y(TARGET) == 5050
    assert get_total_number_of_shots(TARGET) == 2223

def test_challenge18():
    from challenge18 import SNAILFISH, get_magnitude, get_largest_magnitude
    assert get_magnitude(SNAILFISH) == 3816
    assert get_largest_magnitude(SNAILFISH) == 4819

# 19 takes too long

def test_challenge20():
    from challenge20 import IMAGE_INFO, get_number_of_pixels_lit
    assert get_number_of_pixels_lit(IMAGE_INFO) == 5395
    # part 2 takes 8 seconds - too lon

def test_challenge21():
    from challenge21 import PLAYER1, PLAYER2, get_number_of_universes_won_by_predominant_player, get_losing_score_x_dice_rolls
    assert get_losing_score_x_dice_rolls(PLAYER1, PLAYER2) == 908595
    assert get_number_of_universes_won_by_predominant_player(PLAYER1, PLAYER2) == 91559198282731


def test_challenge22():
    from challenge22 import INSTRUCTIONS, get_cubes_on_in_initialization_area
    assert get_cubes_on_in_initialization_area(INSTRUCTIONS) == 596598
    # part 2 takes too long
