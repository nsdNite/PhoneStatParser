# Python 3
import os

from definitions import telephone_status, write_file


def main() -> None:
    # Initialization:
    file_name = input("Please enter filename to process: ")
    input_folder = os.path.join(os.pardir, "input")
    full_path = os.path.join(input_folder, file_name)
    parsed_file = telephone_status(full_path)
    write_file(parsed_file)
    # Exit program:
    print("Press enter to exit.")
    input()


if __name__ == "__main__":
    main()
