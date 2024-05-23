import argparse
import bcrypt
import os
import shutil

def encode_password(password_input):
    return bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt())

def check_password(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_admin(username, password):
    if admin_exists(username):
        print("Admin already exists.")
    else:
        save_admin_to_database(username , encode_password(password))
        print("Admin created successfully.")

def admin_exists(username):
    username = None
    with open(".\\Manager\\manager.txt") as file:
        for line in file:
            username , password = line.strip().split(',')
    return username != None

def save_admin_to_database(username , encoded_password):
    with open(".\\Manager\\manager.txt" , "w") as file:
        file.write(f"{username},{encoded_password}\n")

def refresh_folder(folder_path):
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
        except OSError as e:
            print(f"Error: {folder_path} : {e.strerror}")

    try:
        os.mkdir(folder_path)
    except OSError as e:
        print(f"Error: {folder_path} : {e.strerror}")
    print(f"Folder '{folder_path}' refreshed successfully.")

def purge_data():
    if input("Are you sure about this?(enter Yes if you are anything else if not): ") == "Yes":
        refresh_folder(".\\Data\\Accounts_data")
        refresh_folder(".\\Data\\Accounts_data\\Users")
        refresh_folder(".\\Data\\Projects_Data")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to manage admin users.")
    parser.add_argument("command", choices=['create-admin' , 'purge-data'], help="Command to execute")
    parser.add_argument("--username", help="Username of the admin user")
    parser.add_argument("--password", help="Password of the admin user")
    args = parser.parse_args()

    if args.command == 'create-admin':
        if args.username and args.password:
            create_admin(args.username, args.password)
    elif args.command == 'purge-data':
        purge_data()
    