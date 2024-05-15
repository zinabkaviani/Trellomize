from .. import globals

from enum import Enum, auto

class Priority(Enum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

class Status(Enum):
    BACKLOG = auto()
    TODO = auto()
    DOING = auto()
    DONE = auto()
    ARCHIVED = auto()

class Task:
    def __init__(self, signed_in_username = "" , candidates_for_assignment = [], random_id = "" , title = "", description = "", start_date = "",\
                end_date = None, assignees = [], priority = Priority.LOW, status = Status.BACKLOG, history = "", comments = []):
        self.__signed_in_username = signed_in_username
        self.__candidates_for_assignment = candidates_for_assignment
        self.__random_id = random_id
        self.__title = title
        self.__description = description
        self.__start_date = start_date
        self.__end_date = end_date
        self.__assignees = assignees
        self.__priority = priority
        self.__status = status
        self.__history = history
        self.__comments = comments

    def __update_file_attributes(self):
        """Updates the Task file with Task attributes"""
        # task_data = {
        #     "signed_in_username" : self.__signed_in_username,
        #     "candidates_for_assignment" : self.__candidates_for_assignment,
        #     "random_id" : random_id
        #     "title" : title
        #     "description" : description
        #     start_date
        # }

    def edit_title(self):
        """sets a new title for task with input"""
    def edit_description(self):
        """Set a new description for task with input"""
        #needs change
        pass
    
    def add_assignees(self):
        """add an assignee for the task"""
        options = [*self.__candidates_for_assignment , "Back"]
        choice = globals.get_arrow_key_input(options=options)
        if(choice != "Back"):
            self.__assignees.append(choice)
            self.__update_file_attributes()
        else:
            return None
    
    def remove_assignees(self):
        """remove an assignee for the task"""
        options = [*self.__candidates_for_assignment , "Back"]
        choice = globals.get_arrow_key_input(options=options)
        self.__update_file_attributes()
    
    def change_priority():
        """changes the urgency of the Task"""
        pass

    def change_status():
        """changes the status of the Task"""
        pass

    def update_history():
        """Updates all activities of the leader and assignees"""
        pass

    def add_comments():
        """the signed in user writes a comment for the task"""
        pass
    
    def remove_comments():
        """the signed in user can delete a comment of their own in the task"""
        pass

    def change_end_time():
        """the signed in user can change the end time if he/she is the leader of the main project"""
        pass

    def task_menu():
        """shows the main menu of the task and options of what the fuck i can do"""
        pass