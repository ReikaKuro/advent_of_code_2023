import re
from sty import fg

aoc_input: str = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''


def hex_to_rgb(hex_value) -> tuple:
    rgb_value = re.findall(r'(.{2})(.{2})(.{2})', hex_value)[0]
    print(f'hex_to_rgb: Converted {hex_value} -> {rgb_value}')
    return rgb_value


def color_text(string, color_hex) -> str:
    R, G, B = hex_to_rgb(color_hex)
    R = int(R, 16)
    G = int(G, 16)
    B = int(B, 16)
    colored_string = f'{fg(R, G, B) + string + fg.rs}'
    print(f'color_text: Example output --> {colored_string}')
    return fg(R, G, B) + string + fg.rs


def define_list_size(instructions) -> tuple:
    max_x_size = 1
    max_y_size = 1
    current_x_size = 1
    current_y_size = 1
    for direction_data in instructions:
        direction = direction_data[0]
        value = int(direction_data[1])
        if direction == 'L':
            current_x_size = current_x_size - value
        elif direction == 'R':
            current_x_size = current_x_size + value
        elif direction == 'U':
            current_y_size = current_y_size - value
        elif direction == 'D':
            current_y_size = current_y_size + value

        max_x_size = current_x_size if current_x_size > max_x_size else max_x_size
        max_y_size = current_y_size if current_y_size > max_y_size else max_y_size
    print(f'define_list_size: List size is = ({max_x_size, max_y_size})')
    return max_x_size, max_y_size


def prepare_hashmap(instructions) -> list:
    list_x, list_y = define_list_size(instructions)
    temp_list: list = []
    for y_value in range(list_y):
        temp_list.append([])
        for x_value in range(list_x):
            temp_list[y_value].append(0)

    print(f'prepare_hashmap: Returning hashmap\n{temp_list}')
    return temp_list


def main(dig_plan) -> None:
    instructions: list = re.findall(r'([A-Z])\s(\d+)\s\(#(.*)\)', dig_plan)
    map = prepare_hashmap(instructions)
    x_start_pos = 0
    y_start_pos = 0
    for dig_direction, dig_length, color in instructions:
        for _ in range(int(dig_length)):
            if dig_direction == 'R':
                x_start_pos += 1
                map[y_start_pos][x_start_pos] = color_text('#', color)
            if dig_direction == 'L':
                x_start_pos -= 1
                map[y_start_pos][x_start_pos] = color_text('#', color)
            if dig_direction == 'D':
                y_start_pos += 1
                map[y_start_pos][x_start_pos] = color_text('#', color)
            if dig_direction == 'U':
                y_start_pos -= 1
                map[y_start_pos][x_start_pos] = color_text('#', color)
    for y in map:
        for index, x in enumerate(y):
            if index == (len(y) - 1):
                print(f'{x}')
            else:
                print(f'{x}', end='')
        #print('\n')


main(aoc_input)
