# Python 3
import json
import re


def telephone_status(filename: str) -> dict:
    statuses = []
    output_dict = {}

    # Parse the file:
    with open(filename, "r") as file:
        lines = file.readlines()
        for i in range(len(lines) - 1):
            current_line = lines[i]
            next_line = lines[i + 1]
            answered_status_line = lines[i - 2]

            # Searching non-answered and busy occurrences
            if "Extension " in current_line:
                result = re.search(pattern_tel, current_line)
                match_tel = result.group()
                match_for_line = re.search(pattern_line, next_line)
                match_for_status = re.search(pattern_status, current_line)
                if match_for_line:
                    match_line = match_for_line.group(1)
                    if match_line == "CALLTR0 ":
                        match_line = "Main Line"
                    if match_line == "CALLTR01 ":
                        match_line = "Backup Line"
                else:
                    pass
                if match_for_status:
                    match_status = match_for_status.group(1)
                    if match_status == "no":
                        match_status = "no answer"
                else:
                    pass
                statuses.append(f"{match_tel} {match_line} {match_status}")

            # Searching for answered calls
            if "dialRR" in current_line and "to Play CID" in next_line:
                match_answered = re.search(pattern_answered, current_line)
                if match_answered:
                    answered_phone = match_answered.group()
                match_ans_line = re.search(pattern_answered_line, answered_status_line)
                answered_line = match_ans_line.group(1)
                if answered_line == "CALLTR0":
                    answered_line = "Main Line"
                if answered_line == "CALLTR01":
                    answered_line = "Backup Line"
                statuses.append(f"{answered_phone} {answered_line} answered")

            # Searching for "user hang up":
            counter_hang = 0
            if "Hang Up" in current_line:
                counter_hang += 1
                statuses.append("Hanged up q-ty ")

    # Calculate telephone status occurrences:
    for status in statuses:
        if status in output_dict:
            output_dict[status] += 1
        else:
            output_dict[status] = 1
    # Sort dictionary:
    output_dict = dict(sorted(output_dict.items()))
    return output_dict


def write_file(output_dict: dict) -> None:
    output_file_name = "result.txt"
    json_data = json.dumps(output_dict, indent=4)

    with open(output_file_name, "w") as output_file:
        output_file.write(json_data)

    print("Success. Please check results.txt")


if __name__ == "__main__":
    # Regex:
    pattern_tel = r"\b\d{8}\b"
    pattern_line = r"Status: (.*?)(?=/)"
    pattern_status = r"\b\d{8}\b\s+(\w+)"
    pattern_answered = r"\b\d{8}\b"
    pattern_answered_line = r"status:\s+(\w+)"
    # Initialization:
    file_name = input("Please enter filename to process: ")
    parsed_file = telephone_status(file_name)
    write_file(parsed_file)
    # Exit program:
    print("Press enter to exit.")
    input()
