from .. import globals

class project :
    def __init__(self, id , title,signed_in_username ,members ,leader , tasks ):
        self.__id = id
        self.__title = title
        self.__signed_in_username = signed_in_username
        self.__members = members
        self.__leader = leader 
        self.__tasks = tasks
        
    
    def add_member(self) :
        """leader can add members via username"""

    def remove_members(self) :
        """leader can remove members by chosing between members list via arrow key"""
        pass

    def dispaly_tasks(self) :
        """display tasks of the project"""
        pass

    def add_tasks(self) :
        """leader can add tasks and allocates them to members """
        pass

    def remove_tasks(self) :
        """leader can remove tasks """ 
        pass
    def choose_task(self) :
        """choose tasks to open the task"""
        pass
    def leave_project(self) :
        """users and leader can leave project"""
        pass

    def project_menu(self) :
        options = ["Add Member" ,"Remove Member" ,"Add_Task" , "Remove Task" ,"Choose Task" ,"Leave Project" , "Back"]
        available_options = [""] 