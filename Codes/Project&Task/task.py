import globals

from enum import Enum, auto

class Comment:
    def __init__(self, user_name, text, date_of_comment, time_of_comment):
        self.__user_name = user_name
        self.__text = text
        self.__date_of_comment = date_of_comment
        self.__time_of_comment = time_of_comment
    
    def __str__(self) -> str:
        """shows the comment in a nice format"""
        
        box_width = 50
        upper_line = '╭' + '-' * (box_width - 2) + '╮'
        lower_line = '╰' + '-' * (box_width - 2) + '╯'
        empty_line = '|' + ' ' * (box_width - 2) + '|'

        
        text_lines = globals.split_text(self.__text, box_width - 3)
        is_signed_in = False
        if self.__user_name == globals.signed_in_username:
            is_signed_in = True
        formatted_comment = ''
        formatted_comment += is_signed_in * 40 * ' ' + upper_line + '\n'
        formatted_comment += is_signed_in * 40 * ' ' + '| {0:<47}|\n'.format(self.__user_name)
        formatted_comment += is_signed_in * 40 * ' ' + empty_line + '\n'

        for line in text_lines:
            formatted_comment += is_signed_in * 40 * ' ' + '| {0:<47}|\n'.format(line.strip())

        formatted_comment += is_signed_in * 40 * ' ' + empty_line + '\n'
        formatted_comment += is_signed_in * 40 * ' ' + '| {0:<47}|\n'.format(self.__date_of_comment + 28 * ' '\
                                                                             + self.__time_of_comment)
        formatted_comment += is_signed_in * 40 * ' ' + lower_line + '\n'

        return formatted_comment

    def get_user_name(self):
        return self.__user_name

    def get_text(self):
        return self.__text
    
    def get_date_of_comment(self):
        return self.__date_of_comment
    
    def get_time_of_comment(self):
        return self.__time_of_comment

    def edit_comment(self):
        """edit the comment sent before"""
        while True:
            print("Edit the comment bellow(cancel with 'Esc'):")
            new_text = globals.get_input_with_cancel(self.__text)
            if new_text == "":
                error_messages =["Error" , "Comments can't be empty.(press anything to continue)"]
                globals.print_message(message=f"{error_messages[0]}: {error_messages[1]}" , color ="red")
                globals.msvcrt.getch()
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

    def __str__(self) -> str:
        pass
    def __update_file_attributes(self):
        """Updates the Task file with Task attributes"""
        task_data = {
            "candidates_for_assignment": self.__candidates_for_assignment,
            "title": self.__title,
            "description": self.__description,
            "start_date": self.__start_date,
            "end_date": self.__end_date,
            "assignees": self.__assignees,
            "priority": self.__priority,
            "status": self.__status,
            "history": self.__history,
            "comments": [comment.__dict__ for comment in self.__comments]
        }
        with open(f"Data\\Projects_Data\\{globals.project_id}\\{self.__random_id}.json" , 'w') as file:
            globals.json.dump(task_data , file)

    def edit_title(self):
        """sets a new title for task with input"""
        input_text = self.__title
        print("Edit the title (cancel with Esc):")
        new_title = globals.get_input_with_cancel(input_text)
        if new_title != None:
            self.__title = new_title
            self.__update_file_attributes()

    def edit_description(self):
        """Set a new description for task with input"""
        input_text = self.__description
        print("Edit the description (cancel with Esc):")
        new_description = globals.get_input_with_cancel(input_text)
        if new_description != None:
            self.__description = new_description
            self.__update_file_attributes()
    
    def add_assignees(self):
        """add an assignee for the task"""
        options = [*self.__candidates_for_assignment]
        options.append("Back")

        indices_list = []
        for assignee_index in range(len(self.__candidates_for_assignment)):
            if self.__candidates_for_assignment[assignee_index] not in self.__assignees:
                indices_list.append(assignee_index)
        indices_list.append(len(options) - 1)

        choice = options[globals.get_arrow_key_input(options=options, available_indices= indices_list)]
        if choice != "Back":
            self.__assignees.append(choice)
            self.__update_file_attributes()
    
    def remove_assignees(self):
        """remove an assignee from the task"""
        options = [*self.__assignees , "Back"]
        indices_list = list(range(len(options)))
        choice = options[globals.get_arrow_key_input(options=options, available_indices=indices_list)]
        #Check if the leader is sure about removing the assignee
        if choice != "Back":
            self.__assignees.remove(choice)
            self.__update_file_attributes()
    
    def change_priority(self):
        """changes the urgency of the Task"""
        options = ["LOW" , "MEDIUM" , "HIGH" , "CRITICAL" , "BACK"]
        available_indices = list(range(len(options)))
        choice = options[globals.get_arrow_key_input(options=options,available_indices=available_indices,display=self)]
        match choice:
            case "LOW":
                self.__priority = Priority.LOW
                self.__update_file_attributes()
            case "MEDIUM":
                self.__priority = Priority.MEDIUM
                self.__update_file_attributes()
            case "HIGH":
                self.__priority = Priority.HIGH
                self.__update_file_attributes()
            case "CRITICAL":
                self.__priority = Priority.CRITICAL
                self.__update_file_attributes()
    
    def change_status(self):
        """changes the status of the Task"""
        options = ["BACKLOG" , "TODO" , "DOING" , "DONE" , "ARCHIVED" , "BACK"]
        available_indices = [0 , 1 , 2 , 3 , 4 , 5]
        choice = options[globals.get_arrow_key_input(options=options, available_indices=available_indices, display=self)]
        match choice:
            case "BACKLOG":
                self.__status =Status.BACKLOG
                self.__update_file_attributes()
            case "TODO":
                self.__status = Status.TODO
                self.__update_file_attributes()
            case "DOING":
                self.__status = Status.DOING
                self.__update_file_attributes()
            case "DONE":
                self.__status = Status.DONE
                self.__update_file_attributes()
            case "ARCHIVED":
                self.__status = Status.ARCHIVED
                self.__update_file_attributes()

    def display_history(self):
        """Displays the history of the Task"""
        #needs logging first

    def update_history(self):
        """Updates all activities of the leader and assignees"""
        
        
    def display_comments(self):
        """Displays all the comments on the Task"""
        display = ""
        for comment in self.__comments:
            display += str(comment) + '\n'
        return display

    def add_comments(self):
        """the signed in user writes a comment for the task"""
        #we need some discussion about how we show this
        print(self.display_comments())
        print("\n\t")
        comment = globals.get_input_with_cancel()
        if comment == None:
            return
        else:
            comment_obj = Comment(text=comment, user_name=globals.signed_in_username,\
                            date_of_comment=str(globals.datetime.datetime.now().date()),\
                            time_of_comment=globals.datetime.datetime.now().time().strftime("%H:%M:%S"))
            self.__comments.append(comment_obj)
            self.__update_file_attributes()
            return comment_obj
        

    def remove_comments(self):
        """the signed in user can delete a comment of their own in the task"""
        available_indices = []
        for i in range(len(self.__comments)):
            if self.__comments[i].get_user_name() == globals.signed_in_username:
                available_indices.append(i)
        if self.__leader == globals.signed_in_username:
            available_indices = list(range(len(self.__comments)))
        available_indices.append(len(self.__comments))
        options = ["\n" + str(comment) for comment in self.__comments]
        chosen_index = globals.get_arrow_key_input(options=[*options, "Back"],\
                                                    available_indices=available_indices)
        if chosen_index == len(self.__comments):
            return
        choice = self.__comments[chosen_index]
        #check if the user is sure to delete that comment
        self.__comments.remove(choice)
        self.__update_file_attributes()

    def edit_comments(self):
        """user can edit the comments they have added"""
        available_indices = []
        for i in range(len(self.__comments)):
            if self.__comments[i].get_user_name() == globals.signed_in_username:
                available_indices.append(i)
        available_indices.append(len(self.__comments))
        options = ["\n" + str(comment) for comment in self.__comments]
        chosen_index = globals.get_arrow_key_input(options=[*options, "Back"],\
                                                    available_indices=available_indices)
        if chosen_index == len(self.__comments):
            return
        choice = self.__comments[chosen_index]
        choice.edit_comment()

        self.__update_file_attributes()

    
    def change_end_time(self):
        """the signed in user can change the end time if he/she is the leader of the main project"""
        

    def comments_menu(self):
        """Displays the menu of the available options to do with comments"""
        options = ["Add Comments" , "Remove Comments" , "Edit Comments" , "Back"]
        available_indices = list(range(len(options)))
        if globals.signed_in_username not in [*self.__assignees , self.__leader]:
            available_indices = [3]
        while True:
            choice = options[globals.get_arrow_key_input(options=options, available_indices=available_indices,\
                                                         display=self.display_comments())]
            match choice:
                case "Add Comments":
                    self.add_comments()
                case "Remove Comments":
                    self.remove_comments()
                case "Edit Comments":
                    self.edit_comments()
                case "Back":
                    return
                
    def task_menu(self):
        """Displays the main menu of the task and options of what the the user can do"""
        options = ["Edit Title" , "Edit Description" , "Add Assignees" , "Remove Assignees" ,
                   "Change The Priority Of The Task" , "Change The Status Of The Task" ,
                   "Display The History Of The Task" , "Change The Due Date" , "Comments Section" , "Back"]
        available_indices =[]

        if self.__leader == globals.signed_in_username:
            available_indices = list(range(len(options)))
        elif globals.signed_in_username in self.__assignees:
            available_indices = [0 , 1, 4 , 5 , 6 , 7 , 8 , 9]
        else:
            available_indices = [6 , 8 , 9]
            
        while True:
            choice = options[globals.get_arrow_key_input(options=options, available_indices=available_indices)]
            match choice:
                case "Edit Title":
                    self.edit_title()
                case "Edit Description":
                    self.edit_description()
                case "Add Assignees":
                    self.add_assignees()
                case "Remove Assignees":
                    self.remove_assignees()
                case "Change The Priority Of The Task":
                    self.change_priority()
                case "Change The Status Of The Task":
                    self.change_status()
                case "Display The History Of The Task":
                    self.display_history()
                case "Change The Due Date":
                    self.change_end_time()
                case "Comments Section":
                    self.comments_menu()
                case "Back":
                    return
                