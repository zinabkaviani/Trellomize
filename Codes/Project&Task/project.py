from .. import globals,register
import task

class Project :
    def __init__(self, id , title ,members ,leader , tasks ):
        self.__id = id
        self.__title = title
        self.__members = members
        self.__leader = leader 
        self.__tasks = tasks
        
    def __update_file_attributes(self,*attributes):
        for attribute in attributes :
            with open(f"Data\\Projects_Data\\{self.__id}\\{self.__id}.json" , 'r') as file :
                data = globals.json.load(file)
                match attribute:
                    case "title" :
                        data[attribute] = self.__title
                    case "members" :
                        data[attribute] = self.__members
                    case "tasks" :
                        data[attribute] = self.__tasks
                with open(f"Data\\Projects_Data\\{self.__id}\\{self.__id}.json" , 'w') as updated_file :
                    globals.json.dump(data,updated_file)



    def add_member(self) :
        """leader can add members via username"""
        member = globals.get_input_with_cancel("Please inter member's username to add :")
        if register.check_existing_username(member) :
            self.__members.append(member)
            globals.print_message("Member successfully added to project members",color="green")
        else :
            error_messages =["Error" , "The user dose not have an account."]
            globals.print_message(f"{error_messages[0]}: {error_messages[1]}" , color ="red")

    def remove_members(self) :
        """leader can remove members by chosing between members list via arrow key"""
        indices_list = list(range(len(self.__members)))
        choice = self.__members[globals.get_arrow_key_input(self.__members,indices_list)]
        self.__members.remove(choice)

        self.__update_file_attributes("members")
        
        for task_id in self.__tasks :
        
            with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , 'r') as file :
                data = globals.json.load(file)
                data["assignees"].remove(choice)
        
                with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , 'w') as updated_file :
                    globals.json.dump(data,updated_file)
            
    def dispaly_tasks(self) :
        """display tasks of the project"""
        all_tasks =[]
        for task in self.__tasks:
            with open(f'Data\\Projects_Data\\{self.__id}\\{self.__id}.json', 'r') as file:
                data = globals.json.load(file)
                for task in data:      
                    task_data = [task["id"],task["title"],task["leader"],task["description"],task["status"],task["priority"]]
                    all_tasks.append(task_data)
        
        status_tables = self.display_tables_by_status(all_tasks)
        for table in status_tables.items():
            print(table)
        
    
    def display_tables_by_status(tasks):
        status_tables = {}
        max_table_width = 0
        for status in task.Status:
            tasks_by_status = [task for task in tasks if task["status"] == status]
            if tasks_by_status:
                max_backlog_width = 15
                table = globals.create_status_table(status,tasks_by_status,max_backlog_width)
                status_tables[status] = table
                max_table_width = max(max_table_width, len(table.split('\n')[2]))
        return status_tables
    
    def add_tasks(self) :
        """leader can add tasks and allocates them to members """
        title = globals.get_input_with_cancel("Please inter a title for the task : ")
        des = globals.get_input_with_cancel("Please inter a title for the task : ")
        start_time = globals.get_current_time()
        end_time = globals.get_added_time(start_time , days=1)
        rand_id = globals.generate_random_id(self.__tasks)
        
        with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{rand_id}.json" , "w") as file :
            data ={
                "candidates_for_assignment" : self.__members,
                "title" : title,
                "description" : des,
                "start_date" : start_time,
                "end_date" : end_time,
                "assignees" : [],
                "priority" : task.Priority.LOW,
                "status" : task.Status.BACKLOG,
                # "history" : "" ,
                "comments" : []
            }
            globals.json.dump(data,file)

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
            choice = available_tasks[globals.get_arrow_key_input(options=available_tasks,available_indices= available_indices)]         
            
            if choice != "Back":
                input = globals.get_arrow_key_input(options=["yes","no"],available_indices=[0,1],display="Are you sure about this?")
                if input == 0 :
                    self.__tasks.remove(choice)
                    self.__update_file_attributes("tasks")
                    globals.os.remove(f"Data\\Projects_Data\\{choice}")
                    globals.os.remove(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{choice}.json")
                
                else :
                    choice == "Back"
            else :
                break

    def choose_task(self) :
        """choose tasks to open the task"""

        available_tasks =[]
        
        for task_id in self.__tasks:
            with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{task_id}.json" , "r") as file :
                data= globals.json.load(file)
                available_tasks.append(data["title"] + 10 * ' ' + task_id + '\n'  + data["description"])
        available_tasks.append("Back")
        available_indices = list(range(len(available_tasks)))
        choice = self.__tasks[globals.get_arrow_key_input(options=available_tasks,available_indices= available_indices)]         
        
        with open(f"Data\\Projects_Data\\{self.__id}\\Project_Tasks\\{choice}.json" , "r") as file :
            data= globals.json.load(file)
            candidates_for_assignment = data["candidates_for_assignment"]
            title = data["title"],
            description= data["description"],
            start_time = data["start_date"] ,
            end_time = data["end_date"] ,
            assigness = data["assignees"] ,
            priority = data["priority"] , 
            status = data["status"] ,
            history = data["history"],
            comments = data["comments"]
            task_comments = [task.Comment(comment["account"],comment["text"],comment["date_of_comment"]) for comment in comments]
            
            task.Task(title=title,candidates_for_assignment=candidates_for_assignment,random_id = choice, description=description ,\
                       start_date= start_time , end_date=end_time ,assignees= assigness ,\
                      priority=priority, status= status ,history= history,comments=task_comments )


    def leave_project(self) :
        """users and leader can leave project"""
        print("Are you sure about this?")
        answer = globals.get_input_with_cancel("yes/no")
        if answer == "yes":
            self.leaving_projects()    
        else:
            return
        
    def leaving_projects(self):
        """helping function for leaving the project"""
        if self.__leader == globals.signed_in_username:
            for member in self.__members:
                with open(f"Data\\Accounts_Data\\Users\\{member}.json" , "r") as file :
                    data = globals.json.load(file)
                    data["contributing_projects"].remove(self.__id)
                    with open(f"Data\\Accounts_Data\\Users\\{member}.json" , "w") as updated_file :
                        globals.json.dump(data,updated_file)
            globals.os.remove(f"Data\\Projects_Data\\{self.__id}")

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
            self.__update_file_attributes("members")

    def project_menu(self) :
        while True:
            self.dispaly_tasks() 
            options = ["Add Member" ,"Remove Member" ,"Add_Task" , "Remove Task" ,"Choose Task" ,"Leave Project" , "Exit Project"]
            indices_list = list(range(len(options)))
            choice = None
            if self.__leader == globals.signed_in_username :
                choice = options[globals.get_arrow_key_input(options ,indices_list )]
            else :
                available_indices = [4, 5] 
                choice = options[globals.get_arrow_key_input(options ,available_indices )]

            match choice :
                case "Add Member" :
                    self.add_member() 
                case "Remove Member" :
                    self.remove_members()
                case "Add_Task" :
                    self.add_tasks()
                case "Remove Task" :
                    self.remove_tasks()
                case "Choose Task" :
                    self.choose_task()
                case "Leave Project" :
                    self.leave_project()
                case "Exit Project" :
                    return
                
