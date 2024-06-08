from Codes import globals
from Codes.logfile import logger
from enum import Enum, auto

class Comment:
    def __init__(self, username, text, date_of_comment, time_of_comment):
        self.__username = username
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
        if self.__username == globals.signed_in_username:
            is_signed_in = True
        formatted_comment = ''
        formatted_comment += is_signed_in * 40 * ' ' + upper_line + '\n'
        formatted_comment += is_signed_in * 40 * ' ' + '| {0:<47}|\n'.format(self.__username)
        formatted_comment += is_signed_in * 40 * ' ' + empty_line + '\n'

        for line in text_lines:
            formatted_comment += is_signed_in * 40 * ' ' + '| {0:<47}|\n'.format(line.strip())

        formatted_comment += is_signed_in * 40 * ' ' + empty_line + '\n'
        formatted_comment += is_signed_in * 40 * ' ' + '| {0:<47}|\n'.format(self.__date_of_comment + 28 * ' '\
                                                                             + self.__time_of_comment)
        formatted_comment += is_signed_in * 40 * ' ' + lower_line + '\n'

        return formatted_comment

    def get_username(self):
        return self.__username

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
                error_messages =["Error" , "Comments can't be empty"]
                globals.print_message(message=f"{error_messages[0]}: {error_messages[1]}" , color ="red")
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
        """Shows the task details in a nice format"""
        box_width = 50
        upper_line = '╭' + '-' * (box_width - 2) + '╮'
        lower_line = '╰' + '-' * (box_width - 2) + '╯'
        title_lines = globals.split_text("Task: " + self.__title , 47)
        des_lines = globals.split_text("Description: " + self.__description , 47)
        assignees_lines = globals.split_text("Assignees: " + ', '.join(self.__assignees) , 47)
        empty_line = '| {0:<47}|\n'.format("")
        formatted_task = ''
        formatted_task += upper_line + '\n'
        for line in title_lines:
            formatted_task += '| {0:<47}|\n'.format(line)
        formatted_task += empty_line
        formatted_task += '| {0:<47}|\n'.format("ID: " + self.__random_id)
        formatted_task += empty_line
        for line in des_lines:
            formatted_task += '| {0:<47}|\n'.format(line)
        formatted_task += empty_line
        formatted_task += '| {0:<47}|\n'.format("Start Date: " + self.__start_date)
        formatted_task += empty_line
        formatted_task += '| {0:<47}|\n'.format("End Date: " + (self.__end_date if self.__end_date else "Not set"))
        formatted_task += empty_line
        formatted_task += '| {0:<47}|\n'.format("Leader: " + self.__leader)
        formatted_task += empty_line
        for line in assignees_lines:
            formatted_task += '| {0:<47}|\n'.format(line)
        formatted_task += empty_line
        formatted_task += '| {0:<47}|\n'.format("Priority: " + self.__priority)
        formatted_task += empty_line
        formatted_task += '| {0:<47}|\n'.format("Status: " + self.__status)

        formatted_task += lower_line + '\n'

        return formatted_task
    
    def __update_file_attributes(self):
        """Updates the Task file with Task attributes"""
        task_data = {
            "id": self.__random_id,
            "candidates_for_assignment": self.__candidates_for_assignment,
            "title": self.__title,
            "description": self.__description,
            "start_date": self.__start_date,
            "end_date": self.__end_date,
            "leader": self.__leader,
            "assignees": self.__assignees,
            "priority": self.__priority,
            "status": self.__status,
            "history": self.__history,
            "comments": [{"username": comment.get_username(),
                          "text": comment.get_text(),
                          "date_of_comment": comment.get_date_of_comment(),
                          "time_of_comment": comment.get_time_of_comment()} for comment in self.__comments]
        }
        with open(f"Data\\Projects_Data\\{globals.project_id}\\Project_Tasks\\{self.__random_id}.json" , 'w') as file:
            globals.json.dump(task_data , file)

    def edit_title(self):
        """sets a new title for task with input"""
        input_text = self.__title
        print("Edit the title (cancel with Esc):")
        new_title = globals.get_input_with_cancel(input_text)
        if new_title != None:
            logger.info(f"User {globals.signed_in_username}: edited the title of the Task {self.__random_id}")
            self.update_history(f"User {globals.signed_in_username}: edited the title of the Task {self.__random_id}")
            self.__title = new_title
            self.__update_file_attributes()

    def edit_description(self):
        """Set a new description for task with input"""
        input_text = self.__description
        print("Edit the description (cancel with Esc):")
        new_description = globals.get_input_with_cancel(input_text)
        if new_description != None:
            logger.info(f"User {globals.signed_in_username}: edited the description of the Task {self.__random_id}")
            self.update_history(f"User {globals.signed_in_username}: edited the description of the Task {self.__random_id}")
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

        choice = options[globals.get_arrow_key_input(options=options, available_indices= indices_list,display=self)]
        if choice != "Back":
            logger.info(f"User {globals.signed_in_username}: added the assignee {choice} to the Task {self.__random_id}")
            self.update_history(f"User {globals.signed_in_username}: added the assignee {choice} to the Task {self.__random_id}")
            self.__assignees.append(choice)
            self.__update_file_attributes()
    
    def remove_assignees(self):
        """remove an assignee from the task"""
        options = [*self.__assignees , "Back"]
        indices_list = list(range(len(options)))
        choice = options[globals.get_arrow_key_input(options=options, available_indices=indices_list,display=self)]
        #Check if the leader is sure about removing the assignee
        if choice != "Back":
            logger.info(f"User {globals.signed_in_username}: removed the assignee {choice} from the Task {self.__random_id}")
            self.update_history(f"User {globals.signed_in_username}: removed the assignee {choice} from the Task {self.__random_id}")
            self.__assignees.remove(choice)
            self.__update_file_attributes()
    
    def change_priority(self):
        """changes the urgency of the Task"""
        options = ["LOW" , "MEDIUM" , "HIGH" , "CRITICAL" , "Back"]
        available_indices = list(range(len(options)))
        available_indices.remove(options.index(self.__priority))
        choice = options[globals.get_arrow_key_input(options=options,available_indices=available_indices,display=self)]
        match choice:
            case "LOW":
                self.__priority = Priority.LOW.name
                logger.info(f"User {globals.signed_in_username}: changed the priority of the Task {self.__random_id} from {self.__priority} to LOW")
                self.update_history(f"User {globals.signed_in_username}: changed the priority of the Task {self.__random_id} from {self.__priority} to LOW")
                self.__update_file_attributes()
            case "MEDIUM":
                self.__priority = Priority.MEDIUM.name
                logger.info(f"User {globals.signed_in_username}: changed the priority of the Task {self.__random_id} from {self.__priority} to MEDIUM")
                self.update_history(f"User {globals.signed_in_username}: changed the priority of the Task {self.__random_id} from {self.__priority} to MEDIUM")
                self.__update_file_attributes()
            case "HIGH":
                logger.info(f"User {globals.signed_in_username}: changed the priority of the Task {self.__random_id} from {self.__priority} to HIGH")
                self.update_history(f"User {globals.signed_in_username}: changed the priority of the Task {self.__random_id} from {self.__priority} to HIGH")
                self.__priority = Priority.HIGH.name
                self.__update_file_attributes()
            case "CRITICAL":
                logger.info(f"User {globals.signed_in_username}: changed the priority of the Task {self.__random_id} from {self.__priority} to CRITICAL")
                self.update_history(f"User {globals.signed_in_username}: changed the priority of the Task {self.__random_id} from {self.__priority} to CRITICAL")
                self.__priority = Priority.CRITICAL.name
                self.__update_file_attributes()
    
    def change_status(self):
        """changes the status of the Task"""
        options = ["BACKLOG" , "TODO" , "DOING" , "DONE" , "ARCHIVED" , "Back"]
        available_indices = [0 , 1 , 2 , 3 , 4 , 5]
        available_indices.remove(options.index(self.__status))
        choice = options[globals.get_arrow_key_input(options=options, available_indices=available_indices, display=self)]
        match choice:
            case "BACKLOG":
                logger.info(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to BACKLOG")
                self.update_history(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to BACKLOG")
                self.__status =Status.BACKLOG.name
                self.__update_file_attributes()
            case "TODO":
                logger.info(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to TODO")
                self.update_history(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to TODO")
                self.__status = Status.TODO.name
                self.__update_file_attributes()
            case "DOING":
                logger.info(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to DOING")
                self.update_history(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to DOING")
                self.__status = Status.DOING.name
                self.__update_file_attributes()
            case "DONE":
                logger.info(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to DONE")
                self.update_history(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to DONE")
                self.__status = Status.DONE.name
                self.__update_file_attributes()
            case "ARCHIVED":
                logger.info(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to ARCHIVED")
                self.update_history(f"User {globals.signed_in_username}: changed the status of the Task {self.__random_id} from {self.__status} to ARCHIVED")
                self.__status = Status.ARCHIVED.name
                self.__update_file_attributes()

    def display_history(self):
        """Displays the history of the Task"""
        globals.os.system('cls')
        print(self.__history)
        globals.getch()

    def update_history(self , added_history):
        """Updates all activities of the leader and assignees"""
        self.__history += "\n" + globals.GREEN + str(globals.datetime.datetime.now()) + "| " + globals.RESET + added_history
        
    def display_comments(self):
        """Displays all the comments on the Task"""
        display = ""
        for comment in self.__comments:
            display += str(comment) + '\n'
        return display

    def add_comments(self):
        """the signed in user writes a comment for the task"""
        #we need some discussion about how we show this
        while True:
            print("Enter your comment")
            comment = globals.get_input_with_cancel()
            if comment == None:
                return
            elif comment == "":
                logger.warning(f"User {globals.signed_in_username}: Attempt to send empty comment")
                globals.print_message("Error: comments can't be empty",color= "red")
                continue
            else:
                logger.info(f"User {globals.signed_in_username}: added comment to the Task {self.__random_id}")
                comment_obj = Comment(text=comment, username=globals.signed_in_username,\
                                date_of_comment=str(globals.datetime.datetime.now().date()),\
                                time_of_comment=globals.datetime.datetime.now().time().strftime("%H:%M:%S"))
                self.__comments.append(comment_obj)
                self.__update_file_attributes()
                return comment_obj
        

    def remove_comments(self):
        """the signed in user can delete a comment of their own in the task"""
        available_indices = []
        for i in range(len(self.__comments)):
            if self.__comments[i].get_username() == globals.signed_in_username:
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
        logger.info(f"User {globals.signed_in_username}: removed their comment on the Task {self.__random_id}")
        self.update_history(f"User {globals.signed_in_username}: removed their comment on the Task {self.__random_id}")
        self.__comments.remove(choice)
        self.__update_file_attributes()

    def edit_comments(self):
        """user can edit the comments they have added"""
        available_indices = []
        for i in range(len(self.__comments)):
            if self.__comments[i].get_username() == globals.signed_in_username:
                available_indices.append(i)
        available_indices.append(len(self.__comments))
        options = ["\n" + str(comment) for comment in self.__comments]
        chosen_index = globals.get_arrow_key_input(options=[*options, "Back"],\
                                                    available_indices=available_indices)
        if chosen_index == len(self.__comments):
            return
        choice = self.__comments[chosen_index]
        logger.info(f"User {globals.signed_in_username}: edited their comment on the Task {self.__random_id}")        
        choice.edit_comment()

        self.__update_file_attributes()

    
    def change_end_time(self):
        """the signed in user can change the end time if he/she is the leader of the main project"""
        while True:
            output = None
            print("Please enter your added time in the chosen set:")
            options =["Minutes","Hours","Days","Weeks","Back"]
            time_selection = options[globals.get_arrow_key_input(options=options ,available_indices=[0,1,2,3,4])]
            if time_selection == "Back":
                return
            print("enter the time you want to add :")
            input_value = globals.get_input_with_cancel()
            if input_value is not None:
                if input_value.isdigit():
                    match time_selection:
                        case "Minutes":
                            output = globals.get_added_time(self.__start_date ,minutes=int(input_value))
                        case "Hours":
                            output = globals.get_added_time(self.__start_date ,hours=int(input_value))
                        case "Days":
                            output = globals.get_added_time(self.__start_date ,days=int(input_value))
                        case "Weeks":
                            output = globals.get_added_time(self.__start_date ,weeks=int(input_value))


                    logger.info(f"User {globals.signed_in_username}: added {input_value} {time_selection} to the task {self.__random_id}")
                    self.update_history(f"User {globals.signed_in_username}: added {input_value} {time_selection} to the task {self.__random_id}")
                    self.__end_date = output
                    self.__update_file_attributes()
                else:
                    logger.info(f"User {globals.signed_in_username}: input non digit value for time change")
                    globals.print_message("Error: you need to input digit")
            else:
                return
        
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
            choice = options[globals.get_arrow_key_input(options=options, available_indices=available_indices,display=self)]
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
                