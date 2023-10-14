# Python 3

from definitions import telephone_status, write_file


def main() -> None:
    # Initialization:
    file_name = input("Please enter filename to process: ")
    parsed_file = telephone_status(file_name)
    write_file(parsed_file, file_name)
    # Exit program:
    print("Press enter to exit.")
    input()


if __name__ == "__main__":
    main()
