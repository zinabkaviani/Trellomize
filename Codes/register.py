import bcrypt
import globals
import User.user as user
import re
import os

def encode_password(password_input):
        return bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt())
    
def check_password(entered_password , hashed_password):
        return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)

def check_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

def check_existing_username(username):
            if os.path.exists("Data\\Acounts_Data\\users.txt"):
                with open("Data\\Acounts_Data\\users.txt", "r") as file:
                    for line in file:
                        stored_username, _ = line.strip().split(',')
                        if username == stored_username:
                            return True
            return False
    
def check_existing_email(email_address):
            if os.path.exists("Data\\Acounts_Data\\users.txt"):
                with open("Data\\Acounts_Data\\users.txt", "r") as file:
                    for line in file:
                        _ , sorted_email_address = line.strip().split(',')
                        if email_address == sorted_email_address:
                            return True
            return False

def register():
    username =None
    email_address = None
    password = None
    while True:
        print("pree Esc to exit")

        print("Enter username: ")
        username = globals.get_input_with_cancel()
        if username == None:
            return
        
        print("Enter email address(correct format : name@gmail.com): ")
        email_address = globals.get_input_with_cancel()
        if email_address == None :
            return
        
        print("Enter password: ")
        password = globals.get_input_with_cancel()
        if password == None :
            return
        
        if check_email_format( email_address) :

            if check_existing_username(username):
                error_messages = ["Error", "Username already exists."]
                globals.print_message(f"{error_messages[0]}: {error_messages[1]}", color="red")
            
            elif check_existing_email(email_address) :
                error_messages =["Error" , "Email address already exists."]
                globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")
            
            else:
                with open("Data\\Acounts_Data\\users.txt", "a") as file:
                    file.write(f"{username},{email_address}\n")
                globals.print_message("Account successfully created.", color="green")
                password = encode_password(password)
                break
        else :
            error_messages =["Error" , "Email format is incorrect."]
            globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")

    
    data = {
        "account" :{"username":username ,"email_address":email_address ,"password":password},
        "leading_projects" : [],
        "contributing_projects" : []
    }
    
    with open(f"Data\\Acounts_Data\\Users\\{username}.json","w" ) as file:
        globals.json.dump(data ,file)
    
    
    return user.User(account=user.Account(username=username , email_address = email_address ,password=password),\
                     contributing_projects=[],leading_projects=[])

def Log_in():
    name, password = globalinput("Enter username or email address(email address correct format : name@gmail.com): "),\
          input("Enter password: ")
    
    username = None
    email_address = None

    with open('user.txt', 'r') as file:
            for line in file:
                username , email_address = line.strip().split(',')        
                if "@" in name:
                    if  name == email_address:
                        with open(f"Data\\Acounts_Data\\Users\\{username}.json", 'r') as file:
                            user_data = globals.json.load(file)
                                        
                        if check_password(entered_password=password ,hashed_password= user_data["password"]):
                            return user.User(account=user.Account(username=username , email_address =  user_data["email_address"],\
                                                                    password=encode_password(password)),contributing_projects=[],\
                                                                    leading_projects=[])
                        else :
                            error_messages =["Error" , "Email address or Password is incorrect"]
                            globals.print_message(f"{error_messages[0]}: {error_messages[1]}", color="red")
                                        
                else:
                    if name == username:            
                        with open(f"Data\\Acounts_Data\\Users\\{username}.json", 'r') as file:
                            user_data = globals.json.load(file)
                                        
                        if check_password(entered_password=password ,hashed_password= user_data["password"]):
                            return user.User(account=user.Account(username=username , email_address =  user_data["email_address"],\
                                                                        password=encode_password(password)),contributing_projects=[],\
                                                                    leading_projects=[])
                        else:
                            error_messages =["Error" , "Username or Password is incorrect"]
                            globals.print_message(f"{error_messages[0]}: {error_messages[1]}", color="red")
                                
                

