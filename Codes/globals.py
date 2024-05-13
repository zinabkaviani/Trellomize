import keyboard 
from colored import fg, attr


def get_arrow_key_input(options):
    print("Use arrow keys to select:")
    for option in options:
        print(option)
    selected_index = 0
    while True:
        key_pressed = keyboard.read_key()
        if key_pressed == "up":
            selected_index = (selected_index - 1) % len(options)
        elif key_pressed == "down":
            selected_index = (selected_index + 1) % len(options)
        elif key_pressed == "enter":
            return options[selected_index]
        

def print_message(message, color="white"):
    max_length = len(max(message.split('\n'), key=len))
    border = '╭' + '─' * (max_length + 8) + '╮'

    color_code = fg(color)
    reset_color = attr(0)

    colored_message = f"{color_code}{message}{reset_color}"  # Apply color to the message

    print(border)
    print(f'│ {colored_message:<{max_length}} │')  # Removed color from the border
    print('╰' + '─' * (max_length + 8) + '╯')