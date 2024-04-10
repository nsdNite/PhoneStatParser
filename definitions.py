import json
import re

from constants import LINES_TO_EXCLUDE

pattern_tel = r"\b\d{8}\b"
pattern_line = r"Status: (.*?)(?=/)"
pattern_status = r"\b\d{8}\b\s+(\w+)"
pattern_answered = r"\b\d{8}\b"
pattern_answered_line = r"status:\s+(\w+)"


def telephone_status(filename: str) -> dict:
    statuses = []
    output_dict = {}

    # Removing unnecessary lines:
    temp_file = "temp.txt"

    with open(filename, "r") as file, open(temp_file, "w") as output:
        for line in file:
            if not any(word in line for word in LINES_TO_EXCLUDE):
                output.write(line)

    # Parse the file:
    with open(temp_file, "r") as file:
        lines = file.readlines()
        total_counter = 0
        for i in range(len(lines) - 1):
            current_line = lines[i]
            print(current_line)
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

                match_ans_line = re.search(
                    pattern_answered_line,
                    answered_status_line
                )
                if match_ans_line:
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
                statuses.append("User hanged up Backup Line: ")

            # Searching for total numbers of call
            if "Caller NO." in current_line:
                total_counter += 1

    # Calculate telephone status occurrences:
    for status in statuses:
        if status in output_dict:
            output_dict[status] += 1
        else:
            output_dict[status] = 1
    # Sort dictionary:
    output_dict = dict(sorted(output_dict.items()))
    # Calculate totals:
    main_line_busy = 0
    main_line_na = 0
    main_line_total = 0
    for key, value in output_dict.items():
        if "Main Line busy" in key:
            main_line_busy += value
        if "Main Line no answer" in key:
            main_line_na += value
    for key, value in output_dict.items():
        if "Main Line" in key:
            main_line_total += value
    # Add totals:
    hanged_up_main = total_counter - main_line_total
    totals_dict = {
        "User hanged up Main Line:": hanged_up_main,
        "Total Main Line busy": main_line_busy,
        "Total Main Line no answer: ": main_line_na,
        "Total calls: ": total_counter
    }
    output_dict.update(totals_dict)

    return output_dict


# add sums for Main lines (busy, na)
def write_file(output_dict: dict, filename: str) -> None:
    output_file_name = f"result_{filename}"
    json_data = json.dumps(output_dict, indent=4)

    with open(output_file_name, "w") as output_file:
        output_file.write(json_data)

    print(f"Success. Please check {output_file_name}")
