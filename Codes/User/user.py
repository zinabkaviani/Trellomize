from rich import print
import os
import globals  # Importing keyboard library for arrow key support

def register():
    username = input("Enter username: ")
    email = input("Enter email address: ")
    password = input("Enter password: ")

    if check_existing(username, email):
        print("[bold red]Username or email already exists.[/bold red]")
    else:
        with open("Data\\Acounts_Data\\users.txt", "a") as file:
            file.write(f"{username},{email}\n")
        print("[bold green]Account successfully created.[/bold green]")

def check_existing(username, email):
    if os.path.exists("Data\\Acounts_Data\\users.txt"):
        with open("Data\\Acounts_Data\\users.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                stored_username, stored_email = line.strip().split(',')
                if username == stored_username or email == stored_email:
                    return True
    return False

def change_email(username):
    new_email = input("Enter the new email address: ")
    if not check_existing(username, new_email):
        with open("Data\\Acounts_Data\\users.txt", "r") as file:
            lines = file.readlines()
        with open("Data\\Acounts_Data\\users.txt", "w") as file:
            for line in lines:
                stored_username, stored_email = line.strip().split(',')
                if stored_username == username:
                    file.write(f"{username},{new_email}\n")
                else:
                    file.write(line)
        print("[bold green]Email address updated successfully.[/bold green]")
    else:
        print("[bold red]Email address already exists.[/bold red]")

def register_section():
    options = ["Register", "Change Email"]
    choice = globals.get_arrow_key_input(options)

    if choice == "Register":
        register()
    elif choice == "Change Email":
        username = input("Enter your username: ")
        change_email(username)

