from pprint import pprint

input_data: str = ''
with open('input_day16', 'r') as f:
    input_data = f.read()

map: list = []
output: int = 0

for row in input_data.split('\n'):
    temp = []
    for col in row:
        temp.append(col)

    map.append(temp)

# pprint(map)


def next_direction(direction, X, Y):
    direction = direction
    temp_list = []
    if direction == 'UP' and map[Y][X] == '-' or direction == 'DOWN' and map[Y][X] == '-':
        if X - 1 >= 0:
            if map[Y][X-1] == '|' and energized_map[Y][X-1] == 0 or map[Y][X-1] != '|':
                temp_list.append([X, Y, 'LEFT'])
        if X + 1 < len(map[Y]):
            if map[Y][X+1] == '|' and energized_map[Y][X+1] == 0 or map[Y][X+1] != '|':
                temp_list.append([X, Y, 'RIGHT'])
        return temp_list

    if direction == 'UP' and map[Y][X] == '/' or direction == 'DOWN' and map[Y][X] == '\\':
        direction = 'RIGHT'
        return direction

    if direction == 'UP' and map[Y][X] == '\\' or direction == 'DOWN' and map[Y][X] == '/':
        direction = 'LEFT'
        return direction


    if direction == 'LEFT' and map[Y][X] == '|' or direction == 'RIGHT' and map[Y][X] == '|':
        if Y - 1 >= 0:
            if map[Y-1][X] == '-' and energized_map[Y-1][X] == 0 or map[Y - 1][X] != '-':
                temp_list.append([X, Y, 'UP'])
        if Y + 1 < len(map):
            if map[Y + 1][X] == '-' and energized_map[Y + 1][X] == 0 or map[Y + 1][X] != '-':
                temp_list.append([X, Y, 'DOWN'])
        return temp_list

    if direction == 'LEFT' and map[Y][X] == '\\' or direction == 'RIGHT' and map[Y][X] == '/':
        direction = 'UP'
        return direction

    if direction == 'LEFT' and map[Y][X] == '/' or direction == 'RIGHT' and map[Y][X] == '\\':
        direction = 'DOWN'
        return direction

    return direction


def direction_move(direction, X, Y) -> list[int, int]:
    X = X
    Y = Y
    if direction == 'UP':
        Y -= 1
    if direction == 'DOWN':
        Y += 1
    if direction == 'RIGHT':
        X += 1
    if direction == 'LEFT':
        X -= 1
    # print(f'Returning new X, Y : {X, Y} from direction {direction}')
    return X, Y


# For debug purposes
log_write = open('Day16_2_Logs.txt', 'w')


def main(X=-1, Y=0, direction='RIGHT'):
    log_write.write(f'New Beam from point {X, Y}\n')
    X = X
    Y = Y
    direction = direction
    while True:
        try:
            if X == -1:
                energized_map[Y][X + 1] += 1
            elif Y == -1:
                energized_map[Y+1][X] += 1
            elif X == len(map[0]):
                energized_map[Y][X - 1] += 1
            elif Y == len(map):
                energized_map[Y - 1][X] += 1
            else:
                energized_map[Y][X] += 1

            X, Y = direction_move(direction, X, Y)
            direction = next_direction(direction, X, Y)
            log_write.write(f'New direction {direction} and new point to start X = {X}  Y = {Y} from character "{map[Y][X]}"\n')

            if type(direction) is list:
                return direction

            if X < 0 or Y < 0:
                log_write.write(f'We are outside of table\n')
                return 0

        except IndexError as e:
            log_write.write(f'ERROR 2 {e}, {X, Y}\n')
            return 0


sides_to_check = [[-1, 0, 'RIGHT'], [0, -1, 'DOWN'], [len(map[0]), 0, 'LEFT'], [0, len(map), 'UP']]

try:
    print(f'Starting uber, giga, hard calculations...')
    for side in sides_to_check:
        length_of_side = len(map) if side[2] == 'DOWN' or 'UP' else len(map[0])
        for start in range(0, length_of_side):
            entry_direction: str = side[2]
            entry_x: int = side[0]
            entry_y: int = side[1]
            energized_map: list = []
            to_run: list = []
            run_done: list = []
            this_run_energized: int = 0

            # Start of new Entry to List
            if entry_direction == 'RIGHT':
                to_run.append([entry_x, start, entry_direction])
            if entry_direction == 'LEFT':
                to_run.append([entry_x, start, entry_direction])
            if entry_direction == 'UP':
                to_run.append([start, entry_y, entry_direction])
            if entry_direction == 'DOWN':
                to_run.append([start, entry_y, entry_direction])

            for row in input_data.split('\n'):
                temp = []
                for col in row:
                    temp.append(0)
                energized_map.append(temp)

            log_write.write(f'Starting new Entry to List {to_run[0]}\n')
            log_write.write(f'Map -> {energized_map}\n')
            # Iterations = how many new beams were created during one Entry to List
            iterations = 0
            while to_run:
                if to_run[0] not in run_done:
                    iterations += 1
                    X = to_run[0][0]
                    Y = to_run[0][1]
                    direction = to_run[0][2]
                    log_write.write(f'Moving into direction {direction}, from X = {X}  Y = {Y}\n')
                    new_beams = main(X, Y, direction)
                    log_write.write(f'Ended iteration No. {iterations}\n')
                    if new_beams:
                        for new in new_beams:
                            to_run.append(new)
                run_done.append(to_run[0])
                log_write.write(f'Scenarios to run still: {to_run}\n')
                to_run.pop(0)

            for row in energized_map:
                for col in row:
                    if col != 0:
                        this_run_energized += 1
            log_write.write(f'Energized map at the end of this run {energized_map}\n')
            log_write.write(f'During this run {this_run_energized} points were energized\n')

            count = 0
            for z, row in enumerate(energized_map):
                for k, col in enumerate(row):
                    if col != 0:
                        count += 1
                        log_write.write(f'Energize position --> X = {k}, Y = {z}, No. {count}\n')

            if this_run_energized > output:
                log_write.write(f'New highest amount... Old={output}    New={this_run_energized}\n')
                print(f'New highest amount... Old={output}    New={this_run_energized}')
                output = this_run_energized

        log_write.write(f'Ended iteration for SIDE {side}\n')
        print(f'Ended iteration for SIDE {side}')
        log_write.write(f'Current highest count {output}\n')
        print(f'Current highest count {output}')

except KeyboardInterrupt as e:
    print(f'ERROR {e}')
    print(to_run)


print(f'\nJesus F Christ\nFinal Output = {output}')

