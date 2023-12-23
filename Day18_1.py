import re
import time

from sty import fg

VISUALIZE_DRAWING = True
VISUALIZE_FILLING = True
DRAW_TIME_SLEEP = 0  # Set to 0 for huge arrays
FILL_TIME_SLEEP = 0  # Set to 0 for huge arrays
COLOR_DEBUG = False
DEBUG = False


def hex_to_rgb(hex_value) -> tuple:
    rgb_value = re.findall(r'(.{2})(.{2})(.{2})', hex_value)[0]
    if COLOR_DEBUG:
        print(f'hex_to_rgb: Converted {hex_value} -> {rgb_value}')
    return rgb_value


def color_text(string, color_hex) -> str:
    R, G, B = hex_to_rgb(color_hex)
    R = int(R, 16)
    G = int(G, 16)
    B = int(B, 16)
    colored_string = f'{fg(R, G, B) + string + fg.rs}'
    if COLOR_DEBUG:
        print(f'color_text: Example output --> {colored_string}')
    return colored_string


def print_and_delete(text) -> None:
    MOVE_CURSOR_UP = '\033[1A'
    ERASE = '\x1b[2K'

    print(text)
    print((MOVE_CURSOR_UP + ERASE) * len(text.split('\n')), end='')


def define_list_size(instructions) -> tuple:
    max_x_size: int = 1
    max_y_size: int = 1
    current_x_size = 0
    current_y_size = 0
    max_tilts = {
        'LEFT': 0,
        'RIGHT': 0,
        'UP': 0,
        'DOWN': 0
    }
    for direction_data in instructions:
        direction = direction_data[0]
        value = int(direction_data[1])
        if direction == 'L':
            current_x_size = current_x_size - value
            max_tilts['LEFT'] = current_x_size if current_x_size < max_tilts['LEFT'] else max_tilts['LEFT']
        elif direction == 'R':
            current_x_size = current_x_size + value
            max_tilts['RIGHT'] = current_x_size if current_x_size > max_tilts['RIGHT'] else max_tilts['RIGHT']
        elif direction == 'U':
            current_y_size = current_y_size - value
            max_tilts['UP'] = current_y_size if current_y_size < max_tilts['UP'] else max_tilts['UP']
        elif direction == 'D':
            current_y_size = current_y_size + value
            max_tilts['DOWN'] = current_y_size if current_y_size > max_tilts['DOWN'] else max_tilts['DOWN']
        max_x_size = abs(max_tilts['LEFT']) + max_tilts['RIGHT'] + 1
        max_y_size = abs(max_tilts['UP']) + max_tilts['DOWN'] + 1
    if DEBUG:
        print(f'define_list_size: List size is = ({max_x_size, max_y_size}) for these MAX TILTS {max_tilts}')
    return max_x_size, max_y_size, abs(max_tilts['LEFT']), abs(max_tilts['UP'])


def prepare_hashmap(instructions) -> tuple[list, int, int]:
    list_x, list_y, x_offset, y_offset = define_list_size(instructions)
    temp_list: list = []
    for y_value in range(list_y):
        temp_list.append([])
        for x_value in range(list_x):
            temp_list[y_value].append(0)
    if DEBUG:
        print(f'prepare_hashmap: Returning hashmap\n{temp_list}')
    return temp_list, x_offset, y_offset


def fill_polygon(filled_map) -> list:
    start_points: list = []
    injection_row: int = round(len(filled_map) / 2)
    one_half_iterated = False
    entrance_found = False

    while True:
        for character_index, character in enumerate(filled_map[injection_row]):
            if character_index < len(filled_map[0]) - 1:
                if '#' in str(character) and filled_map[injection_row][character_index + 1] == 0:
                    if '#' in str(filled_map[injection_row - 1][character_index]) \
                            and '#' in str(filled_map[injection_row + 1][character_index]):
                        start_points.append((character_index + 1, injection_row))
                        entrance_found = True
                        break
            else:
                if injection_row == round(len(filled_map) / 2) - 1 and one_half_iterated:
                    raise IndexError('All array has been iterated and could not find the entrance')
                if injection_row < len(filled_map) - 1:
                    injection_row = 1
                    one_half_iterated = True
                else:
                    injection_row += 1
        if entrance_found:
            break

    if DEBUG:
        print(f'fill_polygon: Start Point = {start_points}')
        print(f'fill_polygon: one_half_iterated: {one_half_iterated}')
        x_point, y_point = start_points[0]
        print(f'fill_polygon: {filled_map[y_point][x_point - 1]} -> {filled_map[y_point][x_point]}')

    already_checked: list = []
    new_map: list = filled_map
    for x_point, y_point in start_points:
        if (x_point, y_point) not in already_checked:
            if new_map[y_point + 1][x_point] == 0:
                start_points.append((x_point, y_point + 1))
            if new_map[y_point][x_point + 1] == 0:
                start_points.append((x_point + 1, y_point))
            if new_map[y_point - 1][x_point] == 0:
                start_points.append((x_point, y_point - 1))
            if new_map[y_point][x_point - 1] == 0:
                start_points.append((x_point - 1, y_point))
            new_map[y_point][x_point] = color_text('#', 'ff0000')
            if VISUALIZE_FILLING:
                print_and_delete(convert_to_final_map(new_map))
                time.sleep(FILL_TIME_SLEEP)
        already_checked.append((x_point, y_point))
    return new_map


def convert_to_final_map(map_as_list) -> str:
    final_map = ''
    for row in map_as_list:
        for column_index, column in enumerate(row):
            if column_index == (len(row) - 1):
                final_map += f'{column}\n'
            else:
                final_map += f'{column}'

    return final_map


def main(dig_plan) -> None:
    instructions: list = re.findall(r'([A-Z])\s(\d+)\s\(#(.*)\)', dig_plan)
    dig_plan, x_offset, y_offset = prepare_hashmap(instructions)
    x_start_pos = x_offset
    y_start_pos = y_offset

    for dig_direction, dig_length, color in instructions:
        for _ in range(int(dig_length)):
            if DEBUG:
                print(f'outer line draw: Direction: {dig_direction} Position X {x_start_pos}, Y {y_start_pos}')

            if dig_direction == 'R':
                x_start_pos = (x_start_pos + 1) if x_start_pos < len(dig_plan[0]) - 1 else 0
                dig_plan[y_start_pos][x_start_pos] = color_text('#', color)

            if dig_direction == 'L':
                x_start_pos = (x_start_pos - 1) if x_start_pos != 0 else len(dig_plan[0]) - 1
                dig_plan[y_start_pos][x_start_pos] = color_text('#', color)

            if dig_direction == 'D':
                y_start_pos = (y_start_pos + 1) if y_start_pos < len(dig_plan) - 1 else 0
                dig_plan[y_start_pos][x_start_pos] = color_text('#', color)

            if dig_direction == 'U':
                y_start_pos = (y_start_pos - 1) if y_start_pos != 0 else len(dig_plan) - 1
                dig_plan[y_start_pos][x_start_pos] = color_text('#', color)

            if VISUALIZE_DRAWING:
                print_and_delete(convert_to_final_map(dig_plan))
                time.sleep(DRAW_TIME_SLEEP)

    filled_map = convert_to_final_map(fill_polygon(dig_plan))
    output_part1 = filled_map.count('#')
    print(f'{filled_map}\n\nFinal output = {output_part1}')


if __name__ == '__main__':
    test_input: str = '''R 6 (#70c710)
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

    main(test_input)  # Should be 62

    with open('input_day18_1', 'r') as f:
        aoc_input = f.read()

    # main(aoc_input)  # Should be 28911 for input_day18_1
