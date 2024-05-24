import json
import os
import globals
from globals import print_message
from Project_Task import project

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


class Account:
    
    def __init__(self, username="", email_address="" , password = ""):
        self.__username = username
        self.__email_address = email_address
        self.__password = password
    
    def get_username(self):
        return self.__username

    def get_email_address(self):
        return self.__email_address

    def account_setting_menu(self) :
        option =["Change Email" , "Delete User" , "Sign Out", "Back"]
        indices_list = list(range(len(option)))
        while True :
            choice = option[globals.get_arrow_key_input(option,indices_list)]
            match choice :
                case "Change Email" :
                    self.change_email()
                    return "email changed"
                case "Delete User" :
                    pass
                case "Sign Out" :
                    return "sign out"
                case "Back" :
                    return "back"

    def change_email(self):
            print("Enter the new email address: ")
            new_email = globals.get_input_with_cancel()
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
                globals.getch()
            else:
                error_messages =["Error" , "Email address already exists."]
                if new_email == self.__email_address:
                    error_messages = ["Error" , "This is your Email address"]
                globals.print_message(f"{error_messages[0]}: {error_messages[1]}", color="red")
                globals.getch()



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
        
        """opens the files of both types of projects the user has and then show the details somehow"""
        globals.print_message(message="Leading Projects",color="reset")
        all_leading_projects_data =[]         
        for project in self.__contributing_projects:
            with open(f'Data\\Projects_Data\\{project}\\{project}.json', 'r') as file:
                data = json.load(file)
                for project in data:      
                    project_data = [project["id"],project["title"],project["leader"]]
                    all_leading_projects_data.append(project_data)
        headers=["ID","Title","Leader"]
        print(globals.create_project_table(headers=headers,data=all_leading_projects_data))
        
        
        globals.print_message("Contibuting Projects")
        all_contibuting_projects_data =[]         
        for project in self.__contributing_projects:
            with open(f'Data\\Projects_Data\\{project}\\{project}.json', 'r') as file:
                data = json.load(file)
                for project in data:      
                    project_data = [project["id"],project["title"],project["leader"]]
                    all_contibuting_projects_data.append(project_data)
        headers=["ID","Title","Leader"]
        print(globals.create_project_table(headers=headers,data=all_contibuting_projects_data))
        globals.getch() 
        
    
    def choose_project(self):
        while True:
            options = ['Leading projects' , 'Contributing projects' , 'Exit']
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
        Options = {}
        for project_id in self.__leading_projects:
            with open(f'Data\\Projects_Data\\{project_id}\\{project_id}.json' , 'w') as file:
                Data = json.load(file)
                for key , value in Data:
                    Options[project_id : value]
        #show Options to choose to be added
        project.Project(id="id", title="man" , members=["ma" , "to"] , leader="man" , tasks=["AnIR9r"]).project_menu()

    def choose_contributing_projects(self):
         Options = {}
         for project_id in self.__contributing_projects:
            with open(f'Data\\Projects_Data\\{project_id}\\{project_id}.json' , 'w') as file:
                Data = json.load(file)
                for key , value in Data:
                    Options[project_id : value]
        #show Options to choose to be added
        

    def create_project(self):
        #needs a menu and checking if a project with the same id has been made before
        #and then make a file and other stuff
        pass
    
    def delete_project(self) :
        #delete project from file of projecta , leader and all the members file
        pass

    def user_menu(self) :
        options = ["Display Projects", "Add Project" , "Choose Project" , "Delete Project" , "Account Setting"]
        indices_list = list(range(len(options)))
        while True:
            choice =options[globals.get_arrow_key_input(options,indices_list)]
            match choice :

                case "Display Projects" :
                    self.display_projects()

                case "Add Project" :
                    self.create_project()
                
                case "Choose Project" :
                    self.choose_project()
                
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