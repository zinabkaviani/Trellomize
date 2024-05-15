import os
import msvcrt
from colored import fg, attr


def get_arrow_key_input(options, available_options):

    selected_index = 0
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        print_options(options , selected_index , available_options = options)

        key = ord(msvcrt.getch())
        if key == 72:  # Up arrow key
            selected_index = (selected_index - 1) % len(available_options)
        elif key == 80:  # Down arrow key
            selected_index = (selected_index + 1) % len(available_options)
        elif key == 13:  # Enter key
            return available_options[selected_index]
        

def print_options(options, available_options,selected_index):
    print("Use arrow keys to select:")
    chosen_index = options.find(available_options[selected_index])
    for index, option in enumerate(options):
        if index == chosen_index:
            print("\033[1;32;40m" + f"> {option}" + "\033[m")  # Highlight the selected option in green
        elif option not in available_options :
            print("\033[1;30;40m" + f"> {option}" + "\033[m")
        else:
            print(f"  {option}")
        

def print_message(message, color="white"):
    max_length = len(max(message.split('\n'), key=len))
    border = '╭' + '─' * (max_length + 8) + '╮'

    color_code = fg(color)
    reset_color = attr(0)

    colored_message = f"{color_code}{message}{reset_color}"  # Apply color to the message

    print(border)
    print(f'│ {colored_message:<{max_length}}       │')  # Removed color from the border
    print('╰' + '─' * (max_length + 8) + '╯')

