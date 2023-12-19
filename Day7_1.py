import re

translate_table = str.maketrans('AKQJT', 'EDCBA')

input_data: str = ''
with open('input_day7_1', 'r') as f:
    input_data = f.read()

# input_data: str = '''32T3K 765
# KK677 28
# KTJJT 220
# QQQJA 483
# T55J5 684'''

input_data = input_data.translate(translate_table)


'''
7 = Five of a kind
6 = Four of a kind
5 = Full house
4 = Three of a kind
3 = Two pair
2 = One pair
1 = High card
'''
hand_value_dict: dict = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: []
}

input_list: list = []

for line in input_data.split('\n'):
    data_regex = re.match(r'(.*)\s(.*)', line)
    hand = data_regex.group(1)
    value = data_regex.group(2)
    input_list.append([hand, value])


def sort_cards(cards) -> str:
    temp_list: list = []
    sorted_cards: str = ''
    for card in cards:
        temp_list.append(card)
    temp_list.sort(reverse=True)
    for card in temp_list:
        sorted_cards += card
    print(f'sort_cards: {sorted_cards}')
    return sorted_cards


def how_many_pairs(cards) -> dict:
    cards = cards
    pairs: dict = {}
    summed_pairs: dict = {
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0,
    }
    for card in cards:
        if card not in pairs.keys():
            pairs[card] = 1
        else:
            pairs[card] += 1
    for card in pairs.keys():
        summed_pairs[pairs[card]] += 1
    print(f'how_many_pairs: {summed_pairs}')
    return summed_pairs


def check_if_high_card(cards) -> bool:
    cards = sort_cards(cards)
    for index, card in enumerate(cards):
        if index == len(cards) - 1:
            print(F'check_if_high_card: We are breaking free for index = {index} and len cards = {len(cards) - 1}')
            break
        print(f'check_if_high_card: Hex {card} --> Int {int(card, 16)}   |   Hext {cards[index + 1]} --> Int {int(cards[index + 1], 16)}')
        if not int(card, 16) - 1 == int(cards[index + 1], 16):
            print(f'check_if_high_card: Not high card')
            return False
    return True


def calculate_hand_value(hand) -> int:
    pairs_amount = how_many_pairs(hand)
    if pairs_amount[5] > 0:
        return 7
    if pairs_amount[4] > 0:
        return 6
    if pairs_amount[3] > 0 and pairs_amount[2] > 0:
        return 5
    if pairs_amount[3] > 0:
        return 4
    if pairs_amount[2] == 2:
        return 3
    if pairs_amount[2] == 1:
        return 2
    if pairs_amount[1] == 5:
        return 1
    raise AttributeError(f'Something went wrong and could not define hand value pairs_amount --> {pairs_amount}')


def sort_hand_value_dict() -> None:
    for key in hand_value_dict.keys():
        temp_list = hand_value_dict[key]
        temp_list.sort()
        hand_value_dict[key] = temp_list


def create_new_sorted_list(hand_value_dict) -> list:
    sorted_list: list = [[]]
    for key in hand_value_dict.keys():
        for cards_and_bid in hand_value_dict[key]:
            sorted_list.append(cards_and_bid)

    return sorted_list


def calculate_output_part1(sorted_list) -> int:
    result: int = 0
    for index, cards_and_bid in enumerate(sorted_list[1:], 1):
        cards = cards_and_bid[0]
        bid = cards_and_bid[1]
        print(f'calculate_output_part1: {bid} * {index} = {int(bid) * index}')
        result += int(bid) * index

    return  result


def main() -> None:
    for data in input_list:
        print(data)
        cards = data[0]
        bid = data[1]
        hand_value = calculate_hand_value(cards)
        if value == 1:
            cards = sort_cards(cards)
        hand_value_dict[hand_value].append([cards, bid])
    sort_hand_value_dict()
    new_sorted_list = create_new_sorted_list(hand_value_dict)
    output_part1 = calculate_output_part1(new_sorted_list)
    print(hand_value_dict)
    print(f'Final Output for Part1 is {output_part1}')


# print(input_list)
# print(calculate_hand_value('9ECBD'))
main()
