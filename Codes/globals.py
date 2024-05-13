import os
import msvcrt
from colored import fg, attr


def get_arrow_key_input(options):
    selected_index = 0
    print_options(options, selected_index)

    while True:
        key = ord(msvcrt.getch())
        if key == 72:  # Up arrow key
            selected_index = (selected_index - 1) % len(options)
        elif key == 80:  # Down arrow key
            selected_index = (selected_index + 1) % len(options)
        elif key == 13:  # Enter key
            return options[selected_index]

        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        print_options(options, selected_index)

def print_options(options, selected_index):
    print("Use arrow keys to select:")
    for index, option in enumerate(options):
        if index == selected_index:
            print("\033[1;32;40m" + f"> {option}" + "\033[m")  # Highlight the selected option in green
        else:
            print(f"  {option}")
        

def print_message(message, color="white"):
    max_length = len(max(message.split('\n'), key=len))
    border = '╭' + '─' * (max_length + 8) + '╮'

    color_code = fg(color)
    reset_color = attr(0)

    colored_message = f"{color_code}{message}{reset_color}"  # Apply color to the message

    print(border)
    print(f'│ {colored_message:<{max_length}} │')  # Removed color from the border
    print('╰' + '─' * (max_length + 8) + '╯')