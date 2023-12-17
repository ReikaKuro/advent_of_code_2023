from pprint import pprint

input_data: str = ''
with open('input_day16_3', 'r') as f:
    input_data = f.read()

fake_map = []
map: list = []
energized_map: list = []
output: int = 0

for row in input_data.split('\n'):
    temp = [[], []]
    for number in row:
        temp[0].append(number)
        temp[1].append(0)

    map.append(temp[0])
    fake_map.append(temp[0])
    energized_map.append(temp[1])

# pprint(map)
# pprint(energized_map)


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


def direction_move(direction, X, Y):
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


def main(X=-1, Y=0, direction='RIGHT'):
    print(f'New Start from point {X, Y}')
    X = X
    Y = Y
    direction = direction
    while True:
        try:
            if X == -1:
                energized_map[Y][X + 1] += 1
            # At some point we were getting out of Min Y and this prevents writing on the other side of table
            elif Y == -1:
                energized_map[Y+1][X] += 1
            else:
                energized_map[Y][X] += 1
            X, Y = direction_move(direction, X, Y)
            direction = next_direction(direction, X, Y)
            print(f'New direction {direction} and new point to start X = {X}  Y = {Y} -> {map[Y][X]}')
            if type(direction) is list:
                return direction

            if X < 0 or Y < 0:
                print('We are outside of table')
                return 0
        except IndexError as e:
            print(f'ERROR 2 {e}, {X, Y}')
            return 0


to_run = [[-1, 0, 'RIGHT']]
run_done = []
iterations = 0
try:
    while to_run:
        if to_run[0] not in run_done:
            iterations += 1
            X = to_run[0][0]
            Y = to_run[0][1]
            direction = to_run[0][2]
            print(f'Moving into direction {direction}, from X = {X}  Y = {Y}')
            new_to_run = main(X, Y, direction)
            print(f'Ended iteration No. {iterations}')
            if new_to_run:
                for new in new_to_run:
                    to_run.append(new)
            run_done.append(to_run[0])
        to_run.pop(0)
    print('Jesus F Christ...')

except KeyboardInterrupt as e:
    print(f'ERROR {e}')
    print(to_run)


count = 0
for row in energized_map:
    for number in row:
        if number != 0:
            output += 1
            count += 1
print(f'Final output is: {output}')
