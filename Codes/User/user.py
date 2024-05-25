import json
import os
import globals
import re
from Project_Task import project

def check_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|live|aol)\.com$'
    return re.match(pattern, email) is not None

def delete_project_from_data(project_id):
    with open(f"Data\\Accounts_Data\\{project_id}\\{project_id}.json" , "r") as project_file:
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
                stored_username, _ = line.strip().split(',')
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

from Project_Task import project
from register import check_existing_email ,check_email_format

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
            return "Account deleted"
        
    def delete_user(self):
        if globals.is_admin:
            os.remove("Manager\\managr.txt")
        with open("Data\\Accounts_Data\\users.txt", "r") as file:
            lines = file.readlines()
            with open("Data\\Accounts_Data\\users.txt", "w") as new_file:
                for line in lines:
                    username , _ = line.strip().split(',')
                    if username != self.__username:
                        new_file.write(line)
        with open(f"Data\\Accounts_Data\\{self.__username}.json", "r") as file:
            data = json.load(file)
            for project_id in data["contributing_projects"]:
                with open(f"Data\\Accounts_Data\\{project_id}\\{project_id}.json" , 'r') as project_file:
                    project_data = json.load(project_file)
                    project_data["members"].remove(self.__username)
                    for task_id in project_data["tasks"]:
                        with open(f"Data\\Projects_Data\\{project_id}\\Project_Tasks\\{task_id}.json" , 'r') as file :
                            task_data = globals.json.load(file)
                            task_data["assignees"].remove(self.__username)
                            task_data["candidates_for_assignment"].remove(self.__username)
                            with open(f"Data\\Projects_Data\\{project_id}\\Project_Tasks\\{task_id}.json" , 'w') as updated_file :
                                globals.json.dump(task_data,updated_file)
            for project_id in data["leading_project"]:
                delete_project_from_data(project_id=project_id)
        os.remove(f"Data\\Accounts_Data\\{self.__username}.json")


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
                    return "sign out"
                case "Back" :
                    return "back"
                
    def __update_file_attributes(self):
        user_data = {
            "account": {
                "username": self.__username,
                "email_address": self.__email_address,
                "password": self.__password
            }
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
                globals.print_message()
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
                
                globals.print_message("Email address updated successfully.", color="green")

            else:
                error_messages =["Error" , "Email address already exists."]
                if new_email == self.__email_address:
                    error_messages = ["Error" , "This already is your Email address"]
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
        globals.print_message(message="Leading Projects",color="reset")
        all_leading_projects_data =[]
        for project_id in self.__leading_projects:
            with open(f'Data\\Projects_Data\\{project_id}\\{project_id}.json', 'r') as file:
                data = json.load(file)
                project_data = [data["id"],data["title"],data["leader"]]
                all_leading_projects_data.append(project_data)
        headers=["ID","Title","Leader"]
        print(globals.create_project_table(headers=headers,data=all_leading_projects_data))
        
        
        globals.print_message("Contibuting Projects")
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
            with open(f'Data\\Projects_Data\\{project_id}\\{project_id}.json' , 'w') as file:
                data = json.load(file)
                options.append(f"{data["title"]}      {data["id"]}      {data["leader"]}")
        choice = globals.get_arrow_key_input(options=options, available_indices=list(range(len(options))))    
        if choice != len(options) - 1:
            globals.project_id= self.__contributing_projects[choice]
            with open(f'Data\\Projects_Data\\{self.__contributing_projects[choice]}\\{self.__contributing_projects[choice]}.json' , 'r') as file:
                data = json.load(file)
                return project.Project(id=data["id"],title=data["title"],members=data["members"],leader=data["leader"]\
                                       , tasks=data["tasks"])

    def create_project(self):
        #needs a menu and checking if a project with the same id has been made before
        #and then make a file and other stuff
        pass
    
    def delete_project(self) :
        while True:
            choice = globals.get_arrow_key_input([*self.__leading_projects , "Back"] , list(range(len(self.__leading_projects) + 1)))
            certain = 1 - globals.get_arrow_key_input(["Yes" , "No"] , available_indices= [0 , 1])
            if choice != len(self.__leading_projects):
                if certain:
                    delete_project_from_data(self.__leading_projects[choice])
            else:
                return

    def users_management(self):
        while True:
            choice = globals.get_arrow_key_input(["Activating users" , "Deactivating users" , "Back"] , [0 , 1 , 2])
            if choice == 0:
                self.user_activation()
            elif choice == 1:
                self.user_deactivation()

    @staticmethod
    def user_deactivation():
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
                                if data["is_active"] == 0:
                                    data["is_active"] = 1
                                else:
                                    globals.print_message(f"User {username} has already been deactivated")
                                with open(f"Data\\Accounts_Data\\Users\\{username}.json" , 'w') as new_file:
                                    json.dump(data,new_file)
                            globals.print_message(f"User {username} has been deactivated")
                            return
                globals.print_message(f"No User with the email address {user} Exists")
            else:
                if os.path.exists(f"Data\\Accounts_Data\\Users\\{user}.json"):
                    with open(f"Data\\Accounts_Data\\Users\\{user}.json" , 'r') as file:
                        data = json.load(file)
                        data["is_active"] = 1
                        with open(f"Data\\Accounts_Data\\Users\\{user}.json" , 'w') as new_file:
                            json.dump(data,new_file)
                    globals.print_message(f"User {user} has been deactivated")
                    return
                globals.print_message(f"No User with the username {user} Exists")

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
                                    globals.print_message(f"User {username} has not been deactivated")
                                    return
                                with open(f"Data\\Accounts_Data\\Users\\{username}.json" , 'w') as new_file:
                                    json.dump(data,new_file)
                            globals.print_message(f"User {username} has been activated")
                            return
                globals.print_message(f"No User with the email address {user} Exists")
            else:
                if os.path.exists(f"Data\\Accounts_Data\\Users\\{user}.json"):
                    with open(f"Data\\Accounts_Data\\Users\\{user}.json" , 'r') as file:
                        data = json.load(file)
                        if data["is_active"] == 1:
                            data["is_active"] = 0
                        else:
                            globals.print_message(f"The user with the username {user} has not been deactivated")
                            return
                        with open(f"Data\\Accounts_Data\\Users\\{user}.json" , 'w') as new_file:
                            json.dump(data,new_file)
                    globals.print_message(f"User {user} has been deactivated")
                    return
                globals.print_message(f"No User with the username {user} Exists")


    def user_menu(self) :
        options = ["Display Projects", "Add Project" , "Choose Project" , "Delete Project" , "Account Setting"]
        if globals.user_is_admin:
            options.append("Users Management")
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
                    elif selected_option == "email changed":
                        self.__update_file_attributes()
                    elif selected_option == "Account deleted":
                        del self
                        return
                case "Users Management":
                    self.users_management()