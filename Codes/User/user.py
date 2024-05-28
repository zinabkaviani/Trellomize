import json
import os
from Codes import globals
import re
from Codes.logfile import logger
from Codes.Project_Task import project

def check_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|live|aol)\.com$'
    return re.match(pattern, email) is not None and ',' not in email

def delete_project_from_data(project_id):
    with open(f"Data\\Projects_Data\\{project_id}\\{project_id}.json" , "r") as project_file:
        project_data= json.load(project_file)
        for member in project_data["members"]:
            with open(f"Data\\Accounts_Data\\Users\\{member}.json" , "r") as file :
                task_data = globals.json.load(file)
                task_data["contributing_projects"].remove(project_id)
                with open(f"Data\\Accounts_Data\\Users\\{member}.json" , "w") as updated_file :
                    globals.json.dump(task_data,updated_file)
    globals.shutil.rmtree(f"Data\\Projects_Data\\{project_id}")
    
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
                username , sorted_email_address = line.strip().split(',')
                if email_address == sorted_email_address:
                    return True
    return False

def admin_email_check(user_email_address):

    if os.path.exists("Manager\\manager.json"):
        with open("Manager\\manager.json","r")as file:
            admin_data = globals.json.load(file)
            if user_email_address == admin_data["email_address"]:
                return True
    return False  


class Account:
    
    def __init__(self, username="", email_address="" , password = ""):
        self.__username = username
        self.__email_address = email_address
        self.__password = password
    
    def get_username(self):
        return self.__username

    def get_email_address(self):
        return self.__email_address

    def delete_Account_part(self):
        print("Are you sure about this?")
        choice = globals.get_arrow_key_input(options=["Yes" , "No"],available_indices=[0 , 1])
        if choice == 0:
            self.delete_user()
            if globals.user_is_admin:
                logger.info(f"Admin: Delete account")
            else:
                logger.info(f"User {self.__username}: Delete account")
            return "Account deleted"
        
    def delete_user(self):
        if globals.user_is_admin:
            os.remove("Manager\\managr.txt")
        with open("Data\\Accounts_Data\\users.txt", "r") as file:
            lines = file.readlines()
            with open("Data\\Accounts_Data\\users.txt", "w") as new_file:
                for line in lines:
                    username , _ = line.strip().split(',')
                    if username != self.__username:
                        new_file.write(line)
        with open(f"Data\\Accounts_Data\\Users\\{self.__username}.json", "r") as file:
            data = json.load(file)
            for project_id in data["contributing_projects"]:
                with open(f"Data\\Project_Data\\{project_id}\\{project_id}.json" , 'r') as project_file:
                    project_data = json.load(project_file)
                    project_data["members"].remove(self.__username)
                    for task_id in project_data["tasks"]:
                        with open(f"Data\\Projects_Data\\{project_id}\\Project_Tasks\\{task_id}.json" , 'r') as file :
                            task_data = globals.json.load(file)
                            task_data["assignees"].remove(self.__username)
                            task_data["candidates_for_assignment"].remove(self.__username)
                            with open(f"Data\\Projects_Data\\{project_id}\\Project_Tasks\\{task_id}.json" , 'w') as updated_file :
                                globals.json.dump(task_data,updated_file)
            for project_id in data["leading_projects"]:
                delete_project_from_data(project_id=project_id)
        os.remove(f"Data\\Accounts_Data\\Users\\{self.__username}.json")


    def account_setting_menu(self) :
        option =["Change Email" , "Delete Account" , "Sign Out", "Back"]
        indices_list = list(range(len(option)))
        while True :
            choice = option[globals.get_arrow_key_input(option,indices_list)]
            match choice :
                case "Change Email" :
                    self.change_email()
                case "Delete Account" :
                    return self.delete_Account_part()
                case "Delete User" :
                    return self.delete_user()
                case "Sign Out" :
                    globals.user_is_admin = False
                    logger.info(f"User {globals.signed_in_username}: Has signed out")
                    return "sign out"
                case "Back" :
                    return "back"
                
    def __update_file_attributes(self):
        with open(f"Data\\Accounts_Data\\Users\\{self.__username}.json", "r") as file:
            user_data = json.load(file)
            user_data["account"] = {
                "username": self.__username,
                "email_address": self.__email_address,
                "password": self.__password
            }
        with open(f"Data\\Accounts_Data\\Users\\{self.__username}.json", "w") as file:
            json.dump(user_data, file)

    def change_email(self):
            print("Enter the new email address: ")
            new_email = globals.get_input_with_cancel()
            
            if new_email == None:
                return
            if not check_email_format(new_email):
                error_messages =["Error" , "Email format is incorrect."]
                logger.info(f"User {self.__username}: input incorrect email format")
                globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color="red")
                return

            if not check_existing_email(new_email):
                with open("Data\\Accounts_Data\\users.txt", "r") as file:
                    lines = file.readlines()
                with open("Data\\Accounts_Data\\users.txt", "w") as file:
                    for line in lines:
                        stored_username, _ = line.strip().split(',')
                        if stored_username == self.__username:
                            file.write(f"{self.__username},{new_email}\n")
                        else:
                           file.write(line)
                self.__email_address = new_email
                self.__update_file_attributes()
                if globals.user_is_admin:
                    with open("Manager\\manager.json" , "w") as file:
                        data = {
                            "username": self.__username,
                            "email_address": self.__email_address,
                            "password": self.__password
                            }
                        globals.json.dump(data , file)
                logger.info(f"User {self.__username}: Email address updated successfully")
                globals.print_message("Email address updated successfully.", color="green")

            else:
                log_message = f"User {self.__username}: Email {new_email} already exists can't change email"
                error_messages =["Error" , "Email address already exists."]
                if new_email == self.__email_address:
                    log_message = f"User {self.__username}: attempt to change email to its self"
                    error_messages = ["Error" , "This already is your Email address"]
                logger.warning(log_message)
                globals.print_message(f"{error_messages[0]}: {error_messages[1]}", color="red")




class User:
    def __init__(self, account, leading_projects, contributing_projects):
        self.__account = account
        self.__leading_projects = leading_projects
        self.__contributing_projects = contributing_projects
    
    def __del__(self) :
        del self.__account
        self.__leading_projects = None
        self.__contributing_projects = None
    
    def __update_file_attributes(self):
        user_data = {
            "account": {"username": self.__account.__dict__["_Account__username"], \
                        "email_address": self.__account.__dict__["_Account__email_address"],\
                        "password": self.__account.__dict__["_Account__password"]},
            "leading_projects": self.__leading_projects,
            "contributing_projects": self.__contributing_projects,
            "is_active": 0
        }
        with open(f"Data\\Accounts_Data\\Users\\{self.__account.get_username()}.json" , "w") as file:
            json.dump(user_data , file)
    
    def display_projects(self):
        
        """opens the files of both types of projects the user has and then shows the details"""
        print("Leading Projects:")
        all_leading_projects_data =[]
        for project_id in self.__leading_projects:
            with open(f'Data\\Projects_Data\\{project_id}\\{project_id}.json', 'r') as file:
                data = json.load(file)
                project_data = [data["id"],data["title"],data["leader"]]
                all_leading_projects_data.append(project_data)
        headers=["ID","Title","Leader"]
        print(globals.create_project_table(headers=headers,data=all_leading_projects_data))
        
        
        print("Contributing Projects:")
        all_contributing_projects_data =[]         
        for project in self.__contributing_projects:
            with open(f'Data\\Projects_Data\\{project}\\{project}.json', 'r') as file:
                data = json.load(file)
                project_data = [data["id"],data["title"],data["leader"]]
                all_contributing_projects_data.append(project_data)
        headers=["ID","Title","Leader"]
        print(globals.create_project_table(headers=headers,data=all_contributing_projects_data))
        globals.getch() 
        
    
    def choose_project(self):
        while True:
            options = ['Leading projects' , 'Contributing projects' , 'Back']
            available_indices = [0,1,2]
            choice = options[globals.get_arrow_key_input(options=options , available_indices = available_indices)]
            if choice == 'Leading projects':
                result = self.choose_leading_projects()
                if result != None :
                    return result
            elif choice == 'Contributing projects':
                result = self.choose_contributing_projects()
                if result != None:
                    return result
            else:
                return

    def choose_leading_projects(self):
        options = []
        for project_id in self.__leading_projects:
            with open(f'Data\\Projects_Data\\{project_id}\\{project_id}.json' , 'r') as file:
                data = json.load(file)
                options.append(f"{data["title"]}      {data["id"]}")
        options.append("Back")
        choice = globals.get_arrow_key_input(options=options, available_indices=list(range(len(options))))
        if choice != len(options) - 1:
            globals.project_id = self.__leading_projects[choice]
            with open(f'Data\\Projects_Data\\{self.__leading_projects[choice]}\\{self.__leading_projects[choice]}.json' , 'r') as file:
                data = json.load(file)
                return project.Project(id=data["id"],title=data["title"],members=data["members"],leader=data["leader"]\
                                       , tasks=data["tasks"])

    def choose_contributing_projects(self):
        options = []
        for project_id in self.__contributing_projects:
            with open(f'Data\\Projects_Data\\{project_id}\\{project_id}.json' , 'r') as file:
                data = json.load(file)
                options.append(f"{data["title"]}      {data["id"]}      {data["leader"]}")
        options.append("Back")
        choice = globals.get_arrow_key_input(options=options, available_indices=list(range(len(options))))    
        if choice != len(options) - 1:
            globals.project_id= self.__contributing_projects[choice]
            with open(f'Data\\Projects_Data\\{self.__contributing_projects[choice]}\\{self.__contributing_projects[choice]}.json' , 'r') as file:
                data = json.load(file)
                return project.Project(id=data["id"],title=data["title"],members=data["members"],leader=data["leader"]\
                                       , tasks=data["tasks"])

    def create_project(self):
        print("please inter an ID:")
        id = globals.get_input_with_cancel()
        if id == None:
            return
        if not os.path.exists(f'Data\\Projects_Data\\{id}'):
            print("\nPlease inter a title:")
            title = globals.get_input_with_cancel()
            if title == None:
                return
            os.makedirs(f'Data\\Projects_Data\\{id}')
            os.makedirs(f'Data\\Projects_Data\\{id}\\Project_Tasks')
            with open(f'Data\\Projects_Data\\{id}\\{id}.json',"w") as file:
                data ={
                    "id": id,
                    "title": title,
                    "members": [],
                    "leader": globals.signed_in_username,
                    "tasks":[]
                    }
                json.dump(data,file)
            self.__leading_projects.append(id)
            self.__update_file_attributes()
            logger.info(f"User {globals.signed_in_username}: created the project {id}")
        else:
            logger.warning(f"User {globals.signed_in_username}: attempt to create already existing project")
            error_message = ["Error" ,"This id have been chosen befor"]
            globals.print_message(f"{error_message[0]}: {error_message[1]}",color="red")

    
    def delete_project(self) :
        while True:
            choice = globals.get_arrow_key_input([*self.__leading_projects , "Back"] , list(range(len(self.__leading_projects) + 1)))
            if choice == len(self.__leading_projects):
                return
            certain = 1 - globals.get_arrow_key_input(["Yes" , "No"] , available_indices= [0 , 1])
            if certain:
                logger.info(f"User {globals.signed_in_username}: deleted the project {self.__leading_projects[choice]}")
                delete_project_from_data(self.__leading_projects[choice])
                self.__leading_projects.remove(self.__leading_projects[choice])
                return

    def users_management(self):
        while True:
            choice = globals.get_arrow_key_input(["Activating users" , "Deactivating users" , "Back"] , [0 , 1 , 2])
            if choice == 0:
                self.user_activation()
            elif choice == 1:
                self.user_deactivation()
            else:
                return
    @staticmethod
    def user_deactivation():
        print("Enter a username or email address to deactivate the User: (cancel with Esc):")
        user = globals.get_input_with_cancel()
        if user != None:
            if user == globals.signed_in_username or admin_email_check(user):
                logger.error("Attempt to deactivate admin")
                globals.print_message("You cannot deactivate yourself" , "red")
                return
            if check_email_format(user):
                with open("Data\\Accounts_Data\\users.txt", "r") as file:
                    for line in file:
                        username , sorted_email_address = line.strip().split(',')
                        if user == sorted_email_address:
                            with open(f"Data\\Accounts_Data\\Users\\{username}.json" , 'r') as file:
                                data = json.load(file)
                                if data["is_active"] == 0:
                                    logger.info(f"Admin has deactivated the user {data["username"]}")
                                    globals.print_message(f"User {username} has been deactivated" , color="green")
                                    data["is_active"] = 1
                                else:
                                    logger.warning(f"Attempt to deactivate the user {username} again")
                                    globals.print_message(f"Error: User {username} has already been deactivated", color="red")
                                with open(f"Data\\Accounts_Data\\Users\\{username}.json" , 'w') as new_file:
                                    json.dump(data,new_file)
                            return
                logger.warning(f"No User with the email address {user} Exists")
                globals.print_message(f"Error: No User with the email address {user} Exists", color="red")
            else:
                if os.path.exists(f"Data\\Accounts_Data\\Users\\{user}.json"):
                    with open(f"Data\\Accounts_Data\\Users\\{user}.json" , 'r') as file:
                        data = json.load(file)
                        if data["is_active"] == 0:
                            logger.info(f"User {user} has been deactivated")
                            globals.print_message(f"User {user} has been deactivated", color="green")
                            data["is_active"] = 1
                            with open(f"Data\\Accounts_Data\\Users\\{user}.json" , 'w') as new_file:
                                json.dump(data,new_file)
                        else:
                            logger.warning(f"Attempt to deactivate the user {user} again")
                            globals.print_message(f"Error: User {user} has already been deactivated", color="red")
                            
                    return
                logger.warning(f"No User with the username {user} Exists")
                globals.print_message(f"Error: No User with the username {user} Exists", color="red")

    @staticmethod
    def user_activation():
        print("Enter a username or email address to deactivate the User: (cancel with Esc):")
        user = globals.get_input_with_cancel()
        if user != None:
            if check_email_format(user):
                with open("Data\\Accounts_Data\\users.txt", "r") as file:
                    for line in file:
                        username , sorted_email_address = line.strip().split(',')
                        if user == sorted_email_address:
                            with open(f"Data\\Accounts_Data\\Users\\{username}.json" , 'r') as file:
                                data = json.load(file)
                                if data["is_active"] == 1:
                                    data["is_active"] = 0
                                else:
                                    logger.info(f"User {username} has not been deactivated")
                                    globals.print_message(f"Error: User {username} has not been deactivated")
                                    return
                                with open(f"Data\\Accounts_Data\\Users\\{username}.json" , 'w') as new_file:
                                    json.dump(data,new_file)
                            logger.info(f"User {username} has been activated")
                            globals.print_message(f"User {username} has been activated" , color="green")
                            return
                logger.warning(f"No User with the email address {user} Exists")
                globals.print_message(f"Error: No User with the email address {user} Exists", color="red")
            else:
                if os.path.exists(f"Data\\Accounts_Data\\Users\\{user}.json"):
                    with open(f"Data\\Accounts_Data\\Users\\{user}.json" , 'r') as file:
                        data = json.load(file)
                        if data["is_active"] == 1:
                            data["is_active"] = 0
                        else:
                            globals.print_message(f"Error: The user with the username {user} has not been deactivated" , color="red")
                            return
                        with open(f"Data\\Accounts_Data\\Users\\{user}.json" , 'w') as new_file:
                            json.dump(data,new_file)
                    logger.warning(f"User {user} has been deactivated")
                    globals.print_message(f"Error: User {user} has been deactivated", color="green")
                    return
                logger.warning(f"No User with the username {user} Exists")
                globals.print_message(f"Error: No User with the username {user} Exists" , color="red")


    def user_menu(self) :
        options = ["Display Projects", "Add Project" , "Choose Project" , "Delete Project"]
        if globals.user_is_admin:
            options.append("Users Management")
        options.append("Account Setting")
        indices_list = list(range(len(options)))
        while True:
            choice =options[globals.get_arrow_key_input(options,indices_list)]
            match choice :
                case "Display Projects" :
                    self.display_projects()

                case "Add Project" :
                    self.create_project()
                
                case "Choose Project" :
                    result = self.choose_project()
                    if result != None:
                        result.project_menu()
                
                case "Delete Project" :
                    self.delete_project()

                case "Account Setting" :
                    selected_option =  self.__account.account_setting_menu()
                    if selected_option == "sign out" :
                        del self
                        return 
                    elif selected_option == "back" :
                        continue
                    elif selected_option == "Account deleted":
                        del self
                        return
                case "Users Management":
                    self.users_management()