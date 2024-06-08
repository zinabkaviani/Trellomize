import os
import shutil
import msvcrt
from colored import fg, attr
import json
import string
import random
import time
import datetime
import keyboard

    # Unicode characters for rounded corners and lines
tl = '╭' # top-left
tr = '╮' # top-right
bl = '╰' # bottom-left
br = '╯' # bottom-right
hline = '─' # horizontal line
vline = '│' # vertical line
tj = '┬' # top join
bj = '┴' # bottom join
mj = '┼' # middle join
lj = '├' # left join
rj = '┤' # right join

    # ANSI escape codes for colors
RED = '\033[91m'
YELLOW = '\033[93m' 
MAGENTA = '\033[95m'
CYAN = '\033[96m'
GRAY = '\033[90m'
TURQUOISE = '\033[38;5;45m'
GREEN = '\033[92m'
RESET = '\033[0m'

ascii_art = r'''
 _______  _____    ______   _        _        ____
|_   ___||  __ \  |  ____| | |      | |      / __ \ 
  | |    | |__) | | |__    | |      | |     | |  | | 
  | |    |  _  /  |  __|   | |      | |     | |  | | 
  | |    | | \ \  | |____  | |____  | |____ | |__| | 
  |_|    |_|  \_\ |______| |______| |______| \____/ 
         __  __   _____   ______   ______  
        |  \/  | |_   _| |___  /  |  ____| 
        | \  / |   | |      / /   | |__    
        | |\/| |   | |     / /    |  __|   
        | |  | |  _| |_   / /__   | |____  
        |_|  |_| |_____| /_____|  |______|
'''

user_is_admin = False
signed_in_username = None
project_id = None
task_id =None
stop_loading = False

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
                print("\033[1;32;40m" + f"> {option}" + "\033[m")  # Highlight the selected option in GREEN
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
                    

def print_message(message, color= "reset"):
    max_length = len(max(message.split('\n'), key=len))
    border = '╭' + '─' * (max_length + 8) + '╮'
    color_code = None
    message_lines = message.split('\n')
    if color == "reset":
        color_code = attr(0)
    else:
        color_code = fg(color)
    reset_color = attr(0)
    print("\n")
    print(border)
    for line in message_lines:
        colored_message = f"{color_code}{line}{reset_color}"  # Apply color to the message
        print(f'│ {colored_message:<{max_length}}       │')  # Removed color from the border
    print('╰' + '─' * (max_length + 8) + '╯')
    print("press anything to continue")
    getch()


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

def get_added_time(start_time, **keyword):
    delta = datetime.timedelta(**keyword)
    end_time = datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") + delta
    return end_time.strftime("%Y-%m-%d %H:%M:%S")

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

def create_project_table(headers,data):

    columns =[headers] + data
    col_widths = [max(len(str(item)) for item in col)for col in zip(*columns)]

    def create_row(items,sep = vline):
        row = sep+ sep.join(f" {str(item).center(col_widths[i])} "for i , item in enumerate(items)) + sep 
        return row
    
    def create_separator(left , mid  , right):
        separator = left +mid.join(hline * (width + 2) for width in col_widths) + right
        return separator

    header_top_border = GREEN + tl + tj.join(hline * (w + 2) for w in col_widths) + tr + RESET
    header_row = GREEN + create_row(headers) + RESET
    header_middle_separator = GREEN + lj + mj.join(hline * (w + 2) for w in col_widths) + rj + RESET

    bottom_border = create_separator(bl, bj, br)
    
    table = []
    
    data_rows = []
    for row in data:
        data_rows.append(create_row(row))
        data_rows.append(create_separator(lj, mj, rj))
    if data_rows != []:
        data_rows.pop()
        table = [
        header_top_border, header_row, header_middle_separator,
    ] + data_rows + [bottom_border]
    
    else :
        table = [header_top_border, header_row, GREEN + bottom_border + RESET] 
    return '\n'.join(table)


def create_status_table(status, tasks):
 
    # Color mapping based on priority
    priority_color_map = {
        "LOW": TURQUOISE,
        "MEDIUM": GREEN,
        "HIGH": YELLOW,
        "CRITICAL": RED,
    }

    headers = ["ID","Title", "Priority", "Leader", "Description"]
    data = [[task[0],task[1], task[5], task[2], task[3]] for task in tasks]

    col_widths = [max(len(str(item)) for item in col) for col in zip(*[headers] + data)]

    def create_row(items, color, sep=vline):
        row = color + sep + sep.join(f' {str(item).ljust(col_widths[i])} ' for i, item in enumerate(items)) + sep + RESET
        return row

    def create_separator(left, mid, right, color=RESET):
        separator = color + left + mid.join(hline * (w + 2) for w in col_widths) + right + RESET
        return separator

    status_label = f" Status: {status.name} "
    status_border = tl + status_label + hline * (sum(col_widths) + 3 * len(col_widths) - len(status_label) - 1) + tr
    header_top_border = create_separator(tl, tj, tr)
    header_row = create_row(headers, RESET)
    header_middle_separator = create_separator(lj, mj, rj, RESET)

    data_rows = []
    for row in data:
        color = priority_color_map.get(row[2], RESET)
        data_rows.append(create_row(row, color))
        data_rows.append(create_separator(lj, mj, rj, color))
    if data_rows:
        data_rows.pop()

    bottom_border = create_separator(bl, bj, br)

    table = [
        status_border, header_top_border, header_row, header_middle_separator,
    ] + data_rows + [bottom_border]

    return '\n'.join(table)

def justify_input(input_string, length=10):
    str(input_string)
    if isinstance(input_string, list):
        justified_items = []
        for item in input_string:
            if len(item) <= length:
                justified_items.append(item.ljust(length))
            else:
                justified_items.append(item[:length - 3] + '...')
        return justified_items
    else:
        if len(input_string) <= length:
            return input_string.ljust(length)
        else:
            return input_string[:length - 3] + '...'

def getch():
    """Get a single character from standard input. Does not echo to the screen."""
    return msvcrt.getch()

def reset_terminal_color():
    os.write(1, RESET.encode())

def print_ascii_art_with_color_cycle():
    os.system("cls" if os.name == "nt" else "clear")
    colors = [RED, GREEN, YELLOW, TURQUOISE, MAGENTA] 
    color_index = 0
    while not stop_loading:
        os.write(1, b"\033[H")  # Move cursor to top of screen
        for line in ascii_art.split("\n"):
            os.write(1, colors[color_index].encode() + line.encode() + b"\n")
        os.write(1, RESET.encode())  # Reset the color after printing
        time.sleep(1)
        color_index = (color_index + 1) % len(colors)

def loading_bar(duration=5, length=40):
    for i in range(length + 1):
        percent = int(100 * i / length)
        bar = '█' * i + '-' * (length - i)
        print(f'\r|{bar}| {percent}%', end='')
        time.sleep(duration / length)
    print() 

