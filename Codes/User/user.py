import bcrypt
import json
import os
import globals
from rich import print

class Account:
    
    def __init__(self, username = None , password = None, email_address = None):
        self.__username = username
        self.__password = password
        self.__email_address = email_address

    def get_username(self):
        return self.__username

    def get_email_address(self):
        return self.__email_address

    def encode_password(password_input):
        return bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(entered_password , hashed_password):
        return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)
    
    def save_user_data(self):
        user_data = {
            "username": self.__username,
            "password_hash": self.encode_password(self.__password),  # Save the password hash directly as bytes
            "email": self.__email_address
        }
        with open('Data\\Acount_Data\\user_data.json', 'w') as file:
            json.dump(user_data, file)

    def set_attributes_from_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            for key , value in data:
                setattr(self, key, value)


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

