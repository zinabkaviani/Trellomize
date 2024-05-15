import bcrypt
import json
import os
from .. import globals
from globals import print_message

class Account:
    
    def __init__(self, username="", email_address="" , password = ""):
        self.__username = username
        self.__email_address = email_address
        self.__password = password
    
    def get_username(self):
        return self.__username

    def get_email_address(self):
        return self.__email_address

    @staticmethod
    def encode_password(password_input):
        return bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt())
    
    @staticmethod
    def __check_password(entered_password , hashed_password):
        return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)
    
    def save_account_data(self):
        account_data = {
            "password_hash": self.encode_password(self.__password),  # Save the password hash directly as bytes
            "email": self.__email_address
        }
        if os.path.exists(f'Data\\Acount_Data\\Acounts\\{self.__username}.json'):
            with open(f'Data\\Acount_Data\\Acounts\\{self.__username}.json', 'w') as file:
                json.dump(account_data, file)

    def account_setting_menu(self) :
        option =["Change Email" , "Delete User" , "Sing Out", "Back"]
        while True :
            choice = globals.get_arrow_key_input(option)
            match choice :
                case "Change Email" :
                    self.change_email(self)
                case "Delete User" :
                    pass
                case "Sing Out" :
                    return "sing out"
                case "Back" :
                    return "back"

    def register(self):
            self.__username = input("Enter username: ")
            self.__email_address = input("Enter email address: ")
            self.__password = input("Enter password: ")

            if globals.check_existing_username(self.__username):
                error_messages = [["Error", "Username already exists."]]
                print_message(f"{error_messages[0][0]}: {error_messages[0][1]}", color="red")
            
            elif globals.check_existing_email(self.__email_address) :
                error_messages =[["Error" , "Email address already exists."]]
                print_message(f"{error_messages[0][0]}: {error_messages[0][1]}" , color ="red")
            
            else:
                with open("Data\\Acounts_Data\\users.txt", "a") as file:
                    file.write(f"{self.__username},{self.__email_address}\n")
                print_message("Account successfully created.", color="green")
#import csv
    
    def change_email(self):
           new_email = input("Enter the new email address: ")
           if not self.check_existing_username(self.__username):
               with open("Data\\Acounts_Data\\users.txt", "r") as file:
                   lines = file.readlines()
               with open("Data\\Acounts_Data\\users.txt", "w") as file:
                  for line in lines:
                       stored_username, _ = line.strip().split(',')
                       if stored_username == self.__username:
                           file.write(f"{self.__username},{new_email}\n")
                       else:
                           file.write(line)
               print_message("Email address updated successfully.", color="green")
           else:
               print_message("Username already exists.", color="red")

    def register_section(self):
            options = ["Register", "Change Email"]
            choice = globals.get_arrow_key_input(options)

            if choice == "Register":
                self.register()
    #        elif choice == "Change Email":
    #           self.change_email()


class User:
    def __init__(self, username , email_address , password , leading_projects, contributing_projects):
        account = Account(username=username, email_address=email_address, password=password)
        self.__account = account
        self.__leading_projects = leading_projects
        self.__contributing_projects = contributing_projects
    
    def __del__(self) :
        del self.__account
        self.__leading_projects = None
        self.__contributing_projects = None
    
    def display_projects(self):
        #opens the files of both types of projects the user has and then show the details somehow
        #some features can be added such as choosing a project and showing more details about it without
        #going into the project (making an object)
        pass
    
    def choose_project(self):
        while True:
            choice = globals.get_arrow_key_input(['Leading projects' , 'Contributing projects' , 'Exit'])
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
         for project in self.__leading_projects:
            with open(f'Data\\Projects_Data\\{project}.json' , 'w') as file:
                Data = json.load(file)
                for key , value in Data:
                    Options[project : value]
        #show Options to choose to be added
       

    def choose_contributing_projects(self):
         Options = {}
         for project in self.__contributing_projects:
            with open(f'Data\\Projects_Data\\{project}.json' , 'w') as file:
                Data = json.load(file)
                for key , value in Data:
                    Options[project : value]
        #show Options to choose to be added
        

    def create_project(self):
        #needs a menu and checking if a project with the same id has been made before
        #and then make a file and other stuff
        pass
    
    def delete_project() :
        #delete project from file of projecta , leader and all the members file
        pass

    def user_menu(self) :
        options = ["Display Projects", "Add Project" , "Choose Project" , "Delete Project" , "Account Setting"]

        while True:
            choice =globals.get_arrow_key_input(options)
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
                    selected_option =  self.__account.account_setting()
                    if selected_option == "sign out" :
                        del self
                        return 
                    elif selected_option == "back" :
                        continue