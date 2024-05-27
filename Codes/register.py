import bcrypt
import globals
import User.user as user
import re
import os


def encode_password(password_input):
      return bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt())
     
def check_password(entered_password , hashed_password):
       return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|live|aol)\.com$'
    return re.match(pattern, email) is not None and ',' not in email

def is_valid_username(username):
    """username should not have special characters"""
    if not re.match("^[A-Za-z0-9,;]*$", username):
        return False
    return True


def is_username_length_valid( username):
        """"username is at most 15 characters long"""
        if len(username) >= 15:
            return False
        return True

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
    
def admin_username_check(user_username):

    if os.path.exists("Manager\\manager.txt"):
        with open("Manager\\manager.txt","r")as file:
            for line in file:
                admin_username , email = line.strip().split(",")
                if user_username == admin_username:
                    return True
    return False

def admin_email_check(user_email_address):

    if os.path.exists("Manager\\manager.txt"):
        with open("Manager\\manager.txt","r")as file:
            for line in file:
                username , admin_email_address = line.strip().split(",")
                if user_email_address == admin_email_address:
                    return True
    return False  
        
def register():

    username =None
    email_address = None
    password = None
    while True:
        os.system("cls")
        print("pree Esc to exit")
        print("\nEnter username:(correct format : less than 15 character & without special characters(@,#,$...) )")
        username = globals.get_input_with_cancel()
        if username == None:
            return
        if not is_username_length_valid(username=username):
            error_messages =["Error" , "Username should be less than 15 character."]
            globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")
            continue
        if not is_valid_username(username=username):
            error_messages =["Error" , "Username can't have special character."]
            globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")
            continue

        print("\nEnter email address(correct format : name@(gmail|yahoo|outlook|hotmail|live|aol/.com): ")
        email_address = globals.get_input_with_cancel()
        if email_address == None :
            return
        
        print("\nEnter password: ")
        password = globals.get_input_with_cancel()
        if password == None :
            return
        
        if check_email_format( email_address) == True:

            if check_existing_username(username):
                error_messages = ["Error", "Username already exists."]
                globals.print_message(f"{error_messages[0]}: {error_messages[1]}", color="red")
            
            elif check_existing_email(email_address) :
                error_messages =["Error" , "Email address already exists."]
                globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")
    
            else:
                with open("Data\\Accounts_Data\\users.txt", "a") as file:
                    file.write(f"{username},{email_address}\n")
                globals.print_message("Account successfully created.", color="green")
                password = encode_password(password)
                password = password.decode('utf8')
                break
        else :
            error_messages =["Error" , "Email format is incorrect."]
            globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")
          

    
    data = {
        "account" :{"username":username ,"email_address":email_address ,"password":password},
        "leading_projects" : [],
        "contributing_projects" : [],
        "is_active": 0
    }
    
    with open(f"Data\\Accounts_Data\\Users\\{username}.json","w" ) as file:
        globals.json.dump(data ,file)
    globals.signed_in_username = username
    
    return user.User(account=user.Account(username=username , email_address = email_address ,password=password),\
                     contributing_projects=[],leading_projects=[])

def Log_in():
    while True:
        os.system("cls")
        print("Enter username or email address(email address correct format : name@(gmail|yahoo|outlook|hotmail|live|aol.com): ")
        name = globals.get_input_with_cancel()
        if name == None:
            return 
        print("\nEnter password: ")
        password = globals.get_input_with_cancel()
        if password == None:
            return 
        user_data = None
        
        if os.path.exists("Data\\Accounts_Data\\users.txt"):
            with open("Data\\Accounts_Data\\users.txt", 'r') as file:
                if "@" in name:
                    for line in file:
                        username , email_address = line.strip().split(',')        
                        
                        if name == email_address:
                            with open(f"Data\\Accounts_Data\\Users\\{username}.json", 'r') as file:
                                user_data = globals.json.load(file)
                                                
                            if check_password(entered_password=password ,hashed_password= user_data["account"]["password"]):
                                if admin_email_check(name):
                                    globals.user_is_admin = True
                                if user_data["is_active"] == 0:
                                    globals.signed_in_username = username
                                    return user.User(account=user.Account(username=username , email_address = email_address,\
                                                                            password=user_data["account"]["password"]),contributing_projects=user_data["contributing_projects"],\
                                                                            leading_projects=user_data["leading_projects"])
                                
                    error_messages =["Error" , "Email address or Password is incorrect"]
                    if user_data != None:
                        if user_data["is_active"] == 1:
                            error_messages = ["Banned" , "Your account has been deactivated by the admin"]
                    globals.print_message(f"{error_messages[0]}: {error_messages[1]}", color="red")
                    
                    
                                            
                else:
                    for line in file:
                        username , email_address = line.strip().split(',')        
                        
                        if name == username:            
                            with open(f"Data\\Accounts_Data\\Users\\{username}.json", 'r') as file:
                                user_data = globals.json.load(file)
                                                
                            if check_password(entered_password=password ,hashed_password= user_data["account"]["password"]):
                                if admin_username_check(name):
                                    globals.user_is_admin = True
                                if user_data["is_active"] == 0:
                                    globals.signed_in_username = username
                                    return user.User(account=user.Account(username=username , email_address = email_address,\
                                                                        password=user_data["account"]["password"]),contributing_projects=user_data["contributing_projects"],\
                                                                        leading_projects=user_data["leading_projects"])

                    error_messages =["Error" , "Username or Password is incorrect"]
                    if user_data != None:
                        if user_data["is_active"] == 1:
                            error_messages = ["Banned" , "Your account has been deactivated by the admin"]
                    globals.print_message(f"{error_messages[0]}: {error_messages[1]}", color="red")
                    
                                
                

def account_section():
            
    options = ["Sign Up", "Log in" , "Exit"]
    available_indices = [0, 1 , 2]
    user = None
    while True:
        choice = options[globals.get_arrow_key_input(options=options ,available_indices=available_indices)]
        if choice == "Sign Up":
            user = register()
            if user != None:
               user.user_menu()
                    
        elif choice == "Log in":
            user = Log_in()
            if user != None:
                user.user_menu()
        else:
            return


account_section()