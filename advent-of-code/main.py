def read_data(file_name: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    with open(file_name, "r") as file:
        data = file.read()
        rule_list, update_list = data.split("\n\n")
        rule_list = rule_list.split("\n")
        update_list = update_list.split("\n")
    for i, rule in enumerate(rule_list):
        rule_list[i] = tuple([int(item) for item in rule.split("|")])
    for i, update in enumerate(update_list):
        update_list[i] = [int(item) for item in update.split(",")]
    return rule_list, update_list

def part_one(rule_list: list[tuple[int, int]], update_list: list[list[int]]) -> None:
    total = 0
    for update in update_list:
        valid = True
        for x_value, y_value in rule_list:
            if x_value in update and y_value in update:
                for value in update:
                    if value == y_value:
                        valid = False
                        break
                    elif value == x_value:
                        break
                if not valid:
                    break
        if valid:
            total += update[len(update) // 2]
    print(total)

def part_two(rule_list: list[tuple[int, int]], update_list: list[list[int]]) -> None:
    total = 0
    for update in update_list:
        median = 0
        while True:
            valid = True
            for x_value, y_value in rule_list:
                if x_value in update and y_value in update:
                    flag = False
                    for i, value in enumerate(update):
                        if value == y_value:
                            valid = False
                            flag = True
                            y_index = i
                        elif value == x_value:
                            if flag:
                                update[y_index] = x_value
                                update[i] = y_value
                            break
            if valid:
                total += median
                break
            median = update[len(update) // 2]
    print(total)

if __name__ == "__main__":
    file_name = "data.txt"

    rule_list, update_list = read_data(file_name)
    part_one(rule_list, update_list)
    part_two(rule_list, update_list)