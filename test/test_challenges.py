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
