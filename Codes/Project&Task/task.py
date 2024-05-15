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
    def __init__(self, signed_in_username, candidates_for_assignment, random_id, title, description, start_date, end_date = None, assignees = [],\
                priority = Priority.LOW, status = Status.BACKLOG, history = "", comments = []):
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

    def __store_descriptions(self):
        pass

    def edit_description(self):
        """set a new description for task with input"""
        new_description = input("Enter the new description for the task: ")
        if globals.input_canceled:
            return
        else:
            self.__description = new_description

    def add_assignees(self):
        options = [*self.__candidates_for_assignment , "Back"]
        choice = globals.get_arrow_key_input(options=options)
        if(choice != "Back"):
            self.__assignees.append(choice)
            self.__task_data_saver()
        else:
            return None
    
    def remove_assignees(self):
        pass