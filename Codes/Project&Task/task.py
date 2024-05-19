from .. import globals
from enum import Enum, auto
import curses

class Comment:
    def __init__(self, user_name, text, date_of_comment, time_of_comment):
        self.__user_name = user_name
        self.__text = text
        self.__date_of_comment = date_of_comment
        self.__time_of_comment = time_of_comment
    
    def __str__(self) -> str:
        # message = f"{self.__user_name}\n {self.__date_of_comment}          {self.__time_of_comment} \nComment: {self.__text}"
        # max_length = len(max(message.split('\n'), key=len))
        # border = '╭' + '─' * (max_length + 8) + '╮'
        pass


    def edit_comment(self):
        """edit the comment sent before"""
        while True:
            print("Edit the comment bellow(cancel with 'Esc'):")
            print(self.__text, end='')
            new_text = globals.get_input_with_cancel(self.__text)
            if new_text == "":
                error_messages =["Error" , "Comments can't be empty ."]
                globals.print_message(f"{error_messages[0][0]}: {error_messages[0][1]}" , color ="red")
                globals.print_message()
                globals.keyboard.read_event()
            elif new_text == None:
                break
            else:
                self.__text = new_text
                break


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
    def __init__(self,  candidates_for_assignment = [], random_id = "" , title = "", description = "", start_date = "",
                 end_date = None, leader = "", assignees = [], priority = Priority.LOW, status = Status.BACKLOG, history = "",
                 comments = []):
        self.__candidates_for_assignment = candidates_for_assignment
        self.__random_id = random_id
        self.__title = title
        self.__description = description
        self.__start_date = start_date
        self.__end_date = end_date
        self.__leader = leader
        self.__assignees = assignees
        self.__priority = priority
        self.__status = status
        self.__history = history
        self.__comments = comments

    def __update_file_attributes(self):
        """Updates the Task file with Task attributes"""
        task_data = {
            "candidates_for_assignment" : self.__candidates_for_assignment,
            "title" : self.__title,
            "description" : self.__description,
            "start_date" : self.__start_date,
            "end_date" : self.__end_date,
            "assignees" : self.__assignees,
            "priority" : self.__priority,
            "status" : self.__status,
            "history" : self.__history,
            "comments" : [comment.__dict__ for comment in self.__comments]
        }
        with open(f"Data\\Projects_Data\\{globals.project_id}\\{self.__random_id}.json" , 'w') as file:
            globals.json.dump(task_data , file)

    def edit_title(self):
        """sets a new title for task with input"""
        while True:
            input_text = self.__title
            print("Edit the title (cancel with Esc):")
            print(input_text)
            new_title = globals.get_input_with_cancel(input_text)
            if new_title == "":
                error_messages =["Error" , "Task title can't be empty ."]
                globals.print_message(f"{error_messages[0][0]}: {error_messages[0][1]}" , color ="red")
            
                globals.print_message()
                globals.keyboard.read_event()
            elif new_title == None:
                break
            else:
                self.__title = new_title
                break
    
    def edit_description(self):
        """Set a new description for task with input"""
        while True:
            input_text = self.__description
            print("Edit the description (cancel with Esc):")
            print(input_text)
            new_description = globals.get_input_with_cancel(input_text)
            if new_description == None:
                break
            else:
                self.__description = new_description
                break
    
    def add_assignees(self):
        """add an assignee for the task"""
        options = [*self.__candidates_for_assignment , "Back"]
        indices_list = list(range(len(options)))
        choice = options[globals.get_arrow_key_input(options=options, available_indices= indices_list)]
        if choice != "Back":
            self.__assignees.append(choice)
            self.__update_file_attributes()
    
    def remove_assignees(self):
        """remove an assignee from the task"""
        options = [*self.__candidates_for_assignment , "Back"]
        indices_list = list(range(len(options)))
        choice = options[globals.get_arrow_key_input(options=options, available_indices=indices_list)]
        if choice != "Back":
            self.__assignees.remove(choice)
            self.__update_file_attributes()
    
    def change_priority(self):
        """changes the urgency of the Task"""
        pass

    def change_status(self):
        """changes the status of the Task"""
        pass

    def display_history(self):
        """Displays the history of the Task"""
        pass

    def update_history(self):
        """Updates all activities of the leader and assignees"""
        pass

    def display_comments(self):
        """Displays all the comments on the Task"""
        pass

    def add_comments(self):
        """the signed in user writes a comment for the task"""
        pass
    
    def remove_comments(self):
        """the signed in user can delete a comment of their own in the task"""
        pass

    def edit_comments(self):
        """user can edit the comments they have added"""
        pass
    
    def change_end_time(self):
        """the signed in user can change the end time if he/she is the leader of the main project"""
        
    def comments_menu(self):
        """Displays the menu of the available options to do with comments"""
        options = ["Display Comments" , "Add Comments" , "Remove Comments" , "Edit Comments" , "Back"]
        available_indices = options
        if globals.signed_in_username not in [*self.__assignees , self.__leader]:
            available_indices = [0,4]
        while True:
            choice = options[globals.get_arrow_key_input(options=options, available_indice=available_indices)]
            match choice:
                case "Display Comments":
                    self.display_comments()
                case "Add Comments":
                    self.add_comments()
                case "Remove Comments":
                    self.remove_comments()
                case "Edit Comments":
                    self.edit_comments()

    def task_menu(self):
        """Displays the main menu of the task and options of what the the user can do"""
        options = ["Edit Title" , "Edit Description" , "Add Assignees" , "Remove Assignees" ,
                   "Change The Priority Of The Task" , "Change The Status Of The Task" ,
                   "Display The History Of The Task" , "Change The Due Date" , "Comments Section" , "Back"]
        available_indices =[]

        if self.__leader == globals.signed_in_username :
            available_indices = options
        elif globals.signed_in_username in self.__assignees :
            available_indices = ["Edit Title" , "Edit Description" ,
                   "Change The Priority Of The Task" , "Change The Status Of The Task" ,
                   "Display The History Of The Task" , "Change The Due Date" , "Comments Section" , "Back"]
        else :
            available_indices = ["Display The History Of The Task" , "Comments Section" , "Back"]
            
        while True:
            choice = options[globals.get_arrow_key_input(options=options, available_indices=available_indices)]
            match choice:
                case "Edit Title" :
                    self.edit_title()
                case "Edit Description" :
                    self.edit_description()
                case "Add Assignees" :
                    self.add_assignees()
                case "Remove Assignees" :
                    self.remove_assignees()
                case "Change The Priority Of The Task" :
                    self.change_priority()
                case "Change The Status Of The Task" :
                    self.change_status()
                case "Display The History Of The Task" :
                    self.display_history()
                case "Change The Due Date" :
                    self.change_end_time()
                case "Comments Section" :
                    self.comments_menu()
                case "Back" :
                    return