

test_input: str = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''


def parse_input(text: str) -> list:
    return text.strip().split(',')


def calculate_hash_string(hash_string) -> int:
    hash_string_value: int = 0
    for character in hash_string:
        _, hash_string_value = divmod((ord(character) + hash_string_value) * 17, 256)
    return hash_string_value


def main(aoc_input):
    output = 0
    parsed_input: list = parse_input(aoc_input)
    for text in parsed_input:
        output += calculate_hash_string(text)
    return output


if __name__ == '__main__':

    print(f'#Test\n'
          f'Output for Part1: {main(test_input)}')

    with open('input_day15_1', 'r') as f:
        part1_input = f.read()

    print(f'\nOutput for Part1: {main(part1_input)}')
