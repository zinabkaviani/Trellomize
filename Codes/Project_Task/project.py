import globals
from Project_Task import task
import os


def check_existing_username(username,file_path="Data\\Accounts_Data\\users.txt"):
    if os.path.exists(path=file_path):
        with open(file_path, "r") as file:
            for line in file:
                stored_username, email = line.strip().split(',')
                if username == stored_username:
                    return True
    return False


class Project :
    def __init__(self, id , title ,members ,leader , tasks ):
        self.__id = id
        self.__title = title
        self.__members = members
        self.__leader = leader 
        self.__tasks = tasks
    

    def __str__(self):
        box_width = 50
        upper_line = '╭' + '-' * (box_width - 2) + '╮'
        lower_line = '╰' + '-' * (box_width - 2) + '╯'
        members_lines = globals.split_text("Members: " + ', '.join(self.__members),width=47)
        empty_line = '| {0:<47}|\n'.format(" ")
        formatted_project = ''
        formatted_project += upper_line + '\n'
        formatted_project += '| {0:<47}|\n'.format("Project ID: " + globals.justify_input(self.__id,15))
        formatted_project += empty_line
        formatted_project += '| {0:<47}|\n'.format("Title: " + globals.justify_input(self.__title,15))
        formatted_project += empty_line
        formatted_project += '| {0:<47}|\n'.format("Leader: " + self.__leader)
        formatted_project += empty_line
        for line in members_lines:
            formatted_project += '| {0:<47}|\n'.format(line)
        
        formatted_project += lower_line + '\n'

        return formatted_project
    def _update_file_attributes(self):
        data = {
            "id": self.__id,
            "title": self.__title,
            "members": self.__members,
            "leader": self.__leader,
            "tasks": self.__tasks
        }
        with open(f"Data\\Projects_Data\\{self.__id}\\{self.__id}.json" , 'w') as file :
            globals.json.dump(data,file)

    def add_member(self) :
        """leader can add members via username"""
        print("Please inter member's username to add :")
        member = globals.get_input_with_cancel()
        if check_existing_username(member):
            if member not in [*self.__members , self.__leader]:
                self.__members.append(member)
                with open(f"Data\\Accounts_Data\\Users\\{member}.json") as file:
                    user_data = globals.json.load(file)
                    user_data["contributing_projects"].append(self.__id)
                globals.print_message("Member successfully added to project members",color="green")
            else:
                error_messages = ["Error" , "The user is already a member of the Project"]
                globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")
        else :
            error_messages =["Error" , "The user dose not have an account."]
            globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")
        

    def remove_members(self) :
        """leader can remove members by chosing between members list via arrow key"""
        indices_list = list(range(len(self.__members) + 1))
        chosen_index = globals.get_arrow_key_input([*self.__members , "back"],indices_list, display=self.__str__)
        if chosen_index != len(self.__members):
            certain = globals.get_arrow_key_input(["Yes" , "No"] , [0,1],display=self.__str__ + "Are you sure?")
            if certain:
                for task_id in self.__tasks :
                    with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , 'r') as file :
                        data = globals.json.load(file)
                        data["assignees"].remove(self.__members[chosen_index])
                
                        with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , 'w') as updated_file :
                            globals.json.dump(data,updated_file)
                with open(f"Data\\Accounts_Data\\Users\\{self.__members[chosen_index]}.json") as file:
                    user_data = globals.json.load(file)
                    user_data["contributing_projects"].remove(self.__id)
                self.__members.remove(self.__members[chosen_index])
                self.__update_file_attributes()
                globals.print_message("Member successfully removed from project members",color="green")
    
    def display_task_menu(self):
        """a menu for the user to choose what status should be displayed"""
        status_table = self.display_tasks()
        options = ["BACKLOG" , "TODO" ,"DOING" ,"DONE" ,"ARCHIVED","Back"]
        available_indices =[0 ,1 ,2 ,3 ,4 ,5]
        while True:
            choice = options[globals.get_arrow_key_input(options=options , available_indices=available_indices,\
                                                        display= self.__str__+"Please choose the status you want to see its tasks\n")]
            os.system("cls")

            match choice :
                case "BACKLOG":
                    print(status_table["BACKLOG"])
                    print("press any key to return")
                    globals.getch()
                
                case "TODO":
                    print(status_table["TODO"])
                    print("press any key to return")
                    globals.getch()
                case "DOING":
                    print(status_table["DOING"])
                    print("press any key to return")
                    globals.getch()
                case "DONE":
                    print(status_table["DONE"])
                    print("press any key to return")
                    globals.getch()
                case "ARCHIVED":
                    print(status_table["ARCHIVED"])
                    print("press any key to return")
                    globals.getch()

                case "Back":
                    return

    def display_tasks(self) :
        """display tasks of the project"""
        all_tasks =[]
        for task_id in self.__tasks:
            with open(f'Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json', 'r') as file:
                data = globals.json.load(file)      
                all_tasks.append([globals.justify_input(data["id"]), globals.justify_input(data["title"]), self.__leader,globals.justify_input(data["description"]), data["status"], \
                                 data["priority"]])
        
        return  self.display_tables_by_status(tasks=all_tasks)
    
    @staticmethod
    def display_tables_by_status(tasks = []):

        status_tables = {}
        for status in task.Status:
            tasks_by_status = [task for task in tasks if task[4] == status]
            table = globals.create_status_table(status,tasks_by_status)
            status_tables[status.name] = table

        return status_tables
    
    def add_tasks(self) :
        """leader can add tasks and allocates them to members """
        print("Please inter a title for the task : ")
        title = globals.get_input_with_cancel()
        if title == None:
            return
        print("\nPlease inter a description for the task : ")
        des = globals.get_input_with_cancel()
        if des == None:
            return
        start_time = globals.get_current_time()
        end_time = globals.get_added_time(start_time , days=1)
        rand_id = globals.generate_random_id(self.__tasks)
        
        with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{rand_id}.json" , "w") as file :
            data ={
                "id": rand_id,
                "candidates_for_assignment" : self.__members,
                "title" : title,
                "description" : des,
                "start_date" : start_time,
                "end_date" : end_time,
                "leader" : globals.signed_in_username,
                "assignees" : [],
                "priority" : task.Priority.LOW.name,
                "status" : task.Status.BACKLOG.name,
                "history" : "" ,
                "comments" : []
            }
            globals.json.dump(data,file)
        self.__tasks.append(rand_id)
        self.__update_file_attributes()

    def remove_tasks(self) :
        
        """leader can remove tasks """ 

        available_tasks =[]     
        for task_id in self.__tasks:
            with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , "r") as file :
                data= globals.json.load(file)
                available_tasks.append(data["title"] + 10 * ' ' + task_id + '\n'  + data["description"])
        available_tasks.append("Back")
        available_indices = list(range(len(available_tasks)))
        while True:
            chosen_index = globals.get_arrow_key_input(options=available_tasks,available_indices= available_indices,display=self.__str__)
            
            if chosen_index != len(available_tasks) - 1:
                input = globals.get_arrow_key_input(options=["yes","no"],available_indices=[0,1],display=self.__str__ + "Are you sure about this?")
                if input == 0 :
                    globals.os.remove(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{self.__tasks[chosen_index]}.json")
                    self.__tasks.remove(self.__tasks[chosen_index])
                    self.__update_file_attributes()
                    return
            else :
                break

    def choose_task(self) :
        """choose tasks to open the task"""

        available_tasks =[]
        choice = None
        for task_id in self.__tasks:
            with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , "r") as file :
                data= globals.json.load(file)
                available_tasks.append(data["title"] + 10 * ' ' + task_id + '\n'  + data["description"])
        available_tasks.append("Back")
        available_indices = list(range(len(available_tasks)))
        chosen_index = globals.get_arrow_key_input(options=available_tasks,available_indices= available_indices,display=self.__str__)         
        if chosen_index != len(self.__tasks):
            choice = self.__tasks[chosen_index]
        if choice != None:
            with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{choice}.json" , "r") as file :
                data= globals.json.load(file)
                candidates_for_assignment = data["candidates_for_assignment"]
                title = data["title"]
                description= data["description"]
                start_time = data["start_date"]
                end_time = data["end_date"]
                assigness = data["assignees"]
                priority = data["priority"] 
                status = data["status"]
                history = data["history"]
                comments = data["comments"]
                leader = data["leader"]
                task_comments = [task.Comment(comment["username"],comment["text"],comment["date_of_comment"],\
                                              comment["time_of_comment"]) for comment in comments]
                globals.task_id = choice
                return task.Task(title=title,candidates_for_assignment=candidates_for_assignment,random_id = choice, description=description ,\
                                 start_date= start_time , end_date=end_time ,leader= leader, assignees= assigness ,\
                                 priority=priority, status= status ,history= history,comments=task_comments )


    def leave_project(self) :
        """users and leader can leave project"""
        options =["Yes" ,"No"]
        available_indices = [0 ,1]
        answer = options[ globals.get_arrow_key_input(options=options ,available_indices=available_indices,display="Are you sure about this?")]
        if answer == "yes":
            self.leaving_projects()  
            return "leave"   
         
        
    def leaving_projects(self):
        """helping function for leaving the project"""
        if self.__leader == globals.signed_in_username:
            for member in self.__members:
                with open(f"Data\\Accounts_Data\\Users\\{member}.json" , "r") as file :
                    data = globals.json.load(file)
                    data["contributing_projects"].remove(self.__id)
                    with open(f"Data\\Accounts_Data\\Users\\{member}.json" , "w") as updated_file :
                        globals.json.dump(data,updated_file)
            globals.shutil.rmtree(f"Data\\Projects_Data\\{self.__id}")

        elif globals.signed_in_username in self.__members :
            with open(f"Data\\Accounts_Data\\Users\\{globals.signed_in_username}.json" , "r") as file :
                    data = globals.json.load(file)
                    data["contributing_projects"].remove(self.__id)
                    with open(f"Data\\Accounts_Data\\Users\\{globals.signed_in_username}.json" , "w") as updated_file :
                        globals.json.dump(data,updated_file)
            for task_id in self.__tasks :
                with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , "r") as file :
                    data= globals.json.load(file)
                    data["assignees"].remove(globals.signed_in_username)
                    with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , "w") as updated_file :
                        globals.json.dump(data,updated_file)

            self.__members.remove(globals.signed_in_username)
            self.__update_file_attributes()

    def project_menu(self) :
        while True: 
            options = ["Add Member" ,"Remove Member" ,"Display Tasks","Add_Task" , "Remove Task" ,"Choose Task" ,"Leave Project" , "Exit Project"]
            indices_list = list(range(len(options)))
            choice = None
            if self.__leader == globals.signed_in_username :
                choice = options[globals.get_arrow_key_input(options ,indices_list , display=self.__str__())]
            else :
                available_indices = [2 ,5 ,6 ,7] 
                choice = options[globals.get_arrow_key_input(options ,available_indices, display=self.__str__ )]

            match choice :
                case "Add Member":
                    self.add_member() 
                case "Remove Member":
                    self.remove_members()
                case "Display Tasks":
                    self.display_task_menu()
                case "Add_Task":
                    self.add_tasks()
                case "Remove Task":
                    self.remove_tasks()
                case "Choose Task":
                    chosen_task = self.choose_task()
                    if chosen_task != None:
                        chosen_task.task_menu()
                case "Leave Project":
                    if self.leave_project() == "leave":
                        return
                case "Exit Project":
                    return
