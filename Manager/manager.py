import argparse
import bcrypt
import os
import shutil
import re
import json

def check_existing_username(username):
    if os.path.exists("Data\\Accounts_Data\\users.txt"):
        with open("Data\\Accounts_Data\\users.txt", "r") as file:
            for line in file:
                stored_username, email = line.strip().split(',')
                if username == stored_username:
                    return True
    return False


def check_existing_email(email_address):
    if os.path.exists("Data\\Accounts_Data\\users.txt"):
        with open("Data\\Accounts_Data\\users.txt", "r") as file:
            for line in file:
                user_name , sorted_email_address = line.strip().split(',')
                if email_address == sorted_email_address:
                    return True
    return False

def check_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|live|aol)\.com$'
    return re.match(pattern, email) is not None

def is_valid_username(username):
    """username should not have special characters"""
    if not re.match("^[A-Za-z0-9]*$", username):
        return False
    return True

def is_username_length_valid( username):
        """"username is at most 15 characters long"""
        if len(username) > 15:
            return False
        return True
def encode_password(password_input):
    return bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt())

def check_password(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_admin(username, email_address,password):
    if admin_exists():
        print("Admin already exists.")
    elif check_existing_username(username=username):
        
        error_messages = ["Error", "Username already exists."]
        print(f"{error_messages[0]}: {error_messages[1]}")
            
    elif check_existing_email(email_address):

        error_messages =["Error" , "Email address already exists."]
        print(f"{error_messages[0]}: {error_messages[1]}")
    else:
        save_admin_to_database(username=username ,email_address=email_address ,encoded_password=encode_password(password).decode("utf-8"))
        print("Admin created successfully.")

def admin_exists():
    return os.path.exists("manager.json")

def save_admin_to_database(username ,email_address ,encoded_password):
    with open("Manager\\manager.json" , "w") as file:
        data = {"username" :username,
                "email_address" :email_address,
                "password" :encoded_password} 
        json.dump(data,file)

    if os.path.exists("Data\\Accounts_Data\\users.txt"):
        with open("Data\\Accounts_Data\\users.txt" , "a") as file:
            file.write(f"{username},{email_address}\n")
    else :
        with open("Data\\Accounts_Data\\users.txt","w") as file:
            file.write(f"{username},{email_address}\n")

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

def purge_data(username,email,password):

    if input("Are you sure about this?(enter Yes if you are and anything else if not): ") == "Yes":
        refresh_folder(".\\Data\\Accounts_Data")
        refresh_folder(".\\Data\\Accounts_Data\\Users")
        refresh_folder(".\\Data\\Projects_Data")
        with open(".\\Data\\Accounts_Data\\users.txt","w") as file:
            file.write(f"{username},{email}")
        
        data = {
            "account" :{"username":username ,"email_address":email ,"password":password},
            "leading_projects" : [],
            "contributing_projects" : [],
            "is_active": 0
        }
        with open(f".\\Data\\Accounts_Data\\Users\\{username}.json","w" ) as file:
            json.dump(data ,file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script to manage admin user.")
    parser.add_argument("command", choices=['create-admin' , 'purge-data'], help="Command to execute")
    parser.add_argument("--username", help="Username of the admin user")
    parser.add_argument("--password", help="Password of the admin user")
    parser.add_argument("--email_address",help ="email address of the admin user")

    args = parser.parse_args()

    if args.command == 'create-admin':
        if args.username and args.password and args.email_address:
            if is_valid_username(args.username):
                if is_username_length_valid(args.username):
                    if check_email_format(args.email_address):
                        create_admin(args.username,args.email_address, args.password )
                    else:
                        print("Error: email format is incorrect")
                else:
                    print("Error: username can't be more than 15 character")
            else:
                print("Error: username can't contain special characters")
        else:
            print("Error: not enough arguments")

    elif args.command == 'purge-data':
        if args.username and args.email_address and args.password:
            if os.path.exists("Manager\\manager.json"):
                with open("Manager\\manager.json" ,"r") as file :
                    data = json.load(file)
                    if args.username == data["username"] and args.email_address == data["email_address"]:
                        if check_password(entered_password=args.password,hashed_password=data["password"]):
                            purge_data(username=args.username ,email=args.email_address ,password= args.password)
                    else:
                        print("Error: username\\email or password is incorrect")
            else:
                print("Error: username\\email or password is incorrect")

        elif args.username and args.password:
            if os.path.exists("manager.json"):
                with open("Manager\\manager.json" ,"r") as file :
                    data = json.load(file)
                    if args.username == data["username"]:
                        if check_password(entered_password=args.password,hashed_password=data["password"]):
                                purge_data(username=args.username ,email=data["email_address"] ,password= data["password"])
                        else:
                            print("Error: username or password is incorrect")
            else:
                print("Error: username or password is incorrect")

        elif args.email_address and args.password: 
            if os.path.exists("manager.json"):
                with open("Manager\\manager.json" ,"r") as file :
                    data = json.load(file)
                    if args.email_address == data["email"]:
                            if check_password(entered_password=args.password,hashed_password=data["email_address"]):
                                purge_data(username=data["username"] ,email=args.email_address ,password=data["password"])
                            else:
                                print("Error: email address or password is incorrect")
            else:
                print("Error: email address or password is incorrect")

        else:
            print("Error: not enough arguments")
    