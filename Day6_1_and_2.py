import re

input_data: str = '''Time:        49     78     79     80
Distance:   298   1185   1066   1181'''

races: list = []

for line in input_data.split('\n'):
    for index, value in enumerate(re.findall(r'\s\d+', line)):
        if len(races) > index:
            races[index].append(value)
        else:
            races.append([value])


def calculate_best_scenarios(time, distance_to_beat) -> int:
        time: int = time
        distance: int = distance_to_beat
        valid_strategy: int = 0
        current_speed: int = 1
        for index in range(time - 1, 0, -1):
            valid_strategy += 1 if (current_speed * index) > distance else 0
            print(f'Distance to beat {distance}\n'
                  f'Our speed is {current_speed} and we have this amount of time to sprint {index}\n'
                  f'Current valid strategy {valid_strategy}\n'
                  f'We will sprint it in {current_speed * index} and we need to beat {time}\n')
            current_speed += 1

        print(f'Returning valid strategys {valid_strategy}')
        return valid_strategy


output: int = 1
for race in races:
    race_time: int = int(race[0])
    race_distance: int = int(race[1])
    output = output * calculate_best_scenarios(race_time, race_distance)

big_time: str = ''
big_distance: str = ''
for race in races:
    big_time = big_time + race[0].strip()
    big_distance = big_distance + race[1].strip()
output_part2 = calculate_best_scenarios(int(big_time), int(big_distance))
print(f'Final results for part1 is {output} and there is this much possibility per run {races}')
print(f'Final result for part2 is {output_part2} for time = {big_time} and distance = {big_distance}')

