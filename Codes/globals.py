import os
import msvcrt
from colored import fg, attr
import json
import string
import random
import datetime
import keyboard
import register

signed_in_username = "me"
project_id = None
task_id =None


def get_arrow_key_input(options, available_indices, display=""):
    if not available_indices:
        return None 

    selected_index = available_indices[0] 
    def print_options(options, selected_index, available_indices):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        print(display)
        print("Use arrow keys to select:")
        for idx, option in enumerate(options):
            if idx == selected_index:
                print("\033[1;32;40m" + f"> {option}" + "\033[m")  # Highlight the selected option in green
            elif idx in available_indices:
                print(f"  {option}")
            else:
                print("\033[1;30;40m" + f"  {option}" + "\033[m")  # Unavailable option in dim color

    while True:
        print_options(options, selected_index, available_indices)
        key = keyboard.read_event(suppress=True)

        if key.event_type == keyboard.KEY_DOWN:
            if key.name == 'up':
                selected_index = available_indices[(available_indices.index(selected_index) - 1) % len(available_indices)]
            elif key.name == 'down':
                selected_index = available_indices[(available_indices.index(selected_index) + 1) % len(available_indices)]
            elif key.name == 'enter':
                if selected_index is not None:
                    return selected_index
                else:
                    error_message =["Error","No available options to select."]
                    print_message(f"{error_message[0]}: {error_message[1]}",color="red")

def print_message(message, color="white"):
    max_length = len(max(message.split('\n'), key=len))
    border = '╭' + '─' * (max_length + 8) + '╮'

    color_code = fg(color)
    reset_color = attr(0)

    colored_message = f"{color_code}{message}{reset_color}"  # Apply color to the message

    print(border)
    print(f'│ {colored_message:<{max_length}}       │')  # Removed color from the border
    print('╰' + '─' * (max_length + 8) + '╯')


def generate_random_id(existing_ids, length= 6):
    while True:
        # Generate a random ID
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
        # Check if the ID is not in the existing list
        if random_id not in existing_ids:
            return random_id
        
def get_current_time() :
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def get_added_time(start_time , **keyword) :
    end_time = start_time + datetime.timedelta(**keyword)
    return end_time

def get_input_with_cancel(drafted_text = ""):
    print(drafted_text, end='')
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == 'down':
            if event.name == 'esc':
                return None
            elif event.name == 'enter':
                return drafted_text
            elif event.name == 'backspace':
                if len(drafted_text) > 0:
                    print('\b \b', end='', flush=True)
                    drafted_text = drafted_text[:-1]
            elif event.name == 'space':
                print(' ', end='', flush=True)
                drafted_text += ' '
            elif len(event.name) == 1:
                print(event.name, end='', flush=True)
                drafted_text += event.name

def split_text(text, width):
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                if len(word) > width:
                    # Split the word into multiple lines
                    for i in range(0, len(word), width - len(current_line)):
                        current_line += word[i : i + width - len(current_line)]
                        if len(current_line) == width:
                            lines.append(current_line)
                            current_line = ""
                elif len(current_line) + len(word) <= width:
                    current_line += word + " "
                else:
                    lines.append(current_line)
                    current_line = word + " "
            if current_line:
                lines.append(current_line)
            return lines


def account_section():
            
    options = ["Sign Up", "Log in" , "Exit"]
    available_indices = [0, 1 , 2]
    choice = options[globals.get_arrow_key_input(options=options ,available_indices=available_indices)]
    user = None
    while True:
        if choice == "Sign Up":
            user = register.register()
            if user != None:
               user.user_menu()
                    
        elif choice == "Log in":
            user = register.Log_in()
            if user != None:
                user.user_menu()
        else:
            return
                
