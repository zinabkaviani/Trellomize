from .. import globals

class project :
    def __init__(self, id , title,signed_in_username ,members ,leader , tasks ):
        self.__id = id
        self.__title = title
        self.__signed_in_username = signed_in_username
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
        member = input("Please inter member's username to add :")
        if globals.check_existing_username(member) :
            self.__members.append(member)
            globals.print_message("Member successfully added to project members",color="green")
        else :
            error_messages =[["Error" , "The user dose not have an account."]]
            globals.print_message(f"{error_messages[0][0]}: {error_messages[0][1]}" , color ="red")

    def remove_members(self) :
        """leader can remove members by chosing between members list via arrow key"""
        
        choice = globals.get_arrow_key_input(self.__members,self.__members)
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
        pass

    def add_tasks(self) :
        """leader can add tasks and allocates them to members """
        title = input("Please inter a title for the task : ")
        des = input("Please inter a title for the task : ")
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
                # "priority" : 
                # "status" :
                "history" : "",
                "comments" : []
            }
            globals.json.dump(data,file)
            
        
        pass

    def remove_tasks(self) :
        """leader can remove tasks """ 
        choice = globals.get_arrow_key_input(self.__tasks , self.__tasks)
        self.__tasks.remove(choice)
        self.__update_file_attributes("tasks")

    def choose_task(self) :
        """choose tasks to open the task"""
        choice = globals.get_arrow_key_input(self.__tasks,self.__tasks)
        pass
    def leave_project(self) :
        """users and leader can leave project"""
        pass

    def project_menu(self) :
        while True:
            self.dispaly_tasks() 
            options = ["Add Member" ,"Remove Member" ,"Add_Task" , "Remove Task" ,"Choose Task" ,"Leave Project" , "Exit Project"]
            choice = None
            if self.__leader == self.__signed_in_username :
                choice = globals.get_arrow_key_input(options ,options )
            else :
                available_options = ["Choose Task" , "Leave Project"] 
                choice = globals.get_arrow_key_input(options ,available_options )

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
                
