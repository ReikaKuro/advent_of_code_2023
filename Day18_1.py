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
with open('input_day18_1', 'r') as f:
    aoc_input = f.read()


def hex_to_rgb(hex_value) -> tuple:
    rgb_value = re.findall(r'(.{2})(.{2})(.{2})', hex_value)[0]
    # print(f'hex_to_rgb: Converted {hex_value} -> {rgb_value}')
    return rgb_value


def color_text(string, color_hex) -> str:
    R, G, B = hex_to_rgb(color_hex)
    R = int(R, 16)
    G = int(G, 16)
    B = int(B, 16)
    colored_string = f'{fg(R, G, B) + string + fg.rs}'
    # print(f'color_text: Example output --> {colored_string}')
    return colored_string


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
    print(f'define_list_size: List size is = ({max_x_size, max_y_size}) for these MAX TILTS {max_tilts}')
    return max_x_size, max_y_size, abs(max_tilts['LEFT']), abs(max_tilts['UP'])


def prepare_hashmap(instructions) -> tuple[list, int, int]:
    list_x, list_y, x_offset, y_offset = define_list_size(instructions)
    temp_list: list = []
    for y_value in range(list_y):
        temp_list.append([])
        for x_value in range(list_x):
            temp_list[y_value].append(0)

    # print(f'prepare_hashmap: Returning hashmap\n{temp_list}')
    return temp_list, x_offset, y_offset


def calculate_holes(filled_map) -> int:
    filled_map = filled_map
    #TODO
    # Reowrk it into new function that will fill the polygon
    holes: int = 0
    for row_index, row in enumerate(filled_map):
        hashtag_count: int = 0
        last_hashtag: bool = False
        for column_index, column in enumerate(row):
            inside_polygon: bool = True if hashtag_count != 0 else False
            if '#' in str(column):
                holes += 1
                if not last_hashtag:
                    hashtag_count += 1
                    if hashtag_count == 2:
                        hashtag_count = 0
                last_hashtag = True
            elif 0 == column and inside_polygon:
                holes += 1
                filled_map[row_index][column_index] = color_text('@', 'ff0000')
                last_hashtag = False
        print(f'{convert_to_final_map(filled_map)}')

    return holes


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
    #TODO
    # Think about an algorithm for filling spae inside a polygon
    instructions: list = re.findall(r'([A-Z])\s(\d+)\s\(#(.*)\)', dig_plan)
    dig_plan, x_offset, y_offset = prepare_hashmap(instructions)
    x_start_pos = x_offset
    y_start_pos = y_offset
    # steps might delete later
    steps: list= []
    for dig_direction, dig_length, color in instructions:
        for _ in range(int(dig_length)):
            # print(f'Position X {x_start_pos}, Y {y_start_pos}')
            # print(f'{convert_to_final_map(dig_plan)}')
            if dig_direction == 'R':
                x_start_pos = (x_start_pos + 1) if x_start_pos < len(dig_plan[0]) - 1 else 0
                dig_plan[y_start_pos][x_start_pos] = color_text('#', color)
                # Delete steps later
                steps.append((x_start_pos, y_start_pos))
            if dig_direction == 'L':
                x_start_pos = (x_start_pos - 1) if x_start_pos != 0 else len(dig_plan[0]) - 1
                dig_plan[y_start_pos][x_start_pos] = color_text('#', color)
                # Delete steps later
                steps.append((x_start_pos, y_start_pos))
            if dig_direction == 'D':
                y_start_pos = (y_start_pos + 1) if y_start_pos < len(dig_plan) - 1 else 0
                dig_plan[y_start_pos][x_start_pos] = color_text('#', color)
                # Delete steps later
                steps.append((x_start_pos, y_start_pos))
            if dig_direction == 'U':
                y_start_pos = (y_start_pos - 1) if y_start_pos != 0 else len(dig_plan) - 1
                dig_plan[y_start_pos][x_start_pos] = color_text('#', color)
                # Delete steps later
                steps.append((x_start_pos, y_start_pos))
    final_colored_map = convert_to_final_map(dig_plan)
    print(final_colored_map)
    output_part1 = calculate_holes(dig_plan)
    print(f'Final output = {output_part1}')


main(aoc_input)
