import bcrypt
import globals
import User.user as user

def encode_password(password_input):
        return bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt())
    
def check_password(entered_password , hashed_password):
        return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)


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

        if globals.check_email_format( email_address) :

            if globals.check_existing_username(username):
                error_messages = [["Error", "Username already exists."]]
                globals.print_message(f"{error_messages[0][0]}: {error_messages[0][1]}", color="red")
            
            elif globals.check_existing_email(email_address) :
                error_messages =[["Error" , "Email address already exists."]]
                globals.print_message(f"{error_messages[0][0]}: {error_messages[0][1]}" , color ="red")
            
            else:
                with open("Data\\Acounts_Data\\users.txt", "a") as file:
                    file.write(f"{username},{email_address}\n")
                globals.print_message("Account successfully created.", color="green")
                password = encode_password(password)
                break
        else :
            error_messages =[["Error" , "Email format is incorrect."]]
            globals.print_message(f"{error_messages[0][0]}: {error_messages[0][1]}" , color ="red")

    data = {
        "account" :{"username":username ,"email_address":email_address ,"password":password},
        "leading_projects" : [],
        "contributing_projects" : []
    }
    with open(f"Data\\Acounts_Data\\Users\\{username}.json","w" ) as file:
        globals.json.dump(data ,file)
    
    return user.User(account=user.Account(username=username , email_address = email_address ,password=password),\
                     contributing_projects=[],leading_projects=[])

