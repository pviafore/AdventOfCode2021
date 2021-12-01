from common.file_input import read_numbers

Measurements = list[int]
def get_number_of_increasing_measurements(measurements: Measurements) -> int:
    measurement_pairs = zip(measurements, measurements[1:])
    return len([p for p in measurement_pairs if p[1] > p[0]])

def get_number_of_increasing_sliding_windows(
                                        measurements: Measurements) -> int:
    measurement_sums = [sum(w) for w in
                           zip(measurements, measurements[1:], measurements[2:])]
    return get_number_of_increasing_measurements(measurement_sums)



MEASUREMENTS = read_numbers('input/input1.txt')
if __name__ == "__main__":
    print(f"Number of increasing measurments:  "
          f"{get_number_of_increasing_measurements(MEASUREMENTS)}")

    print(f"Number of increasing sliding windows:  "
          f"{get_number_of_increasing_sliding_windows(MEASUREMENTS)}")
