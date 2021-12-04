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
