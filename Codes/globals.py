import keyboard 
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