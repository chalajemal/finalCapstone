import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to read tasks from tasks.txt file
def read_tasks():
    task_list = []
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]
        for t_str in task_data:
            curr_t = {}
            # Split by semicolon and manually add each component
            task_components = t_str.split(";")
            curr_t['username'] = task_components[0]
            curr_t['title'] = task_components[1]
            curr_t['description'] = task_components[2]
            curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
            curr_t['completed'] = True if task_components[5] == "Yes" else False
            task_list.append(curr_t)
    return task_list

# Function to register a new user
def reg_user():
    # Dictionary to hold existing usernames and passwords
    username_password = {}

    # Open the file containing user data
    with open("user.txt", 'r') as user_file:
        # Read data and split into lines
        user_data = user_file.read().split("\n")
        # Iterate through each line
        for user in user_data:
            # Split each line into username and password
            username, password = user.split(';')
            # Add username-password pair to the dictionary
            username_password[username] = password

    # Prompt user for new username and password
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check if passwords match
    if new_password == confirm_password:
        # Check if username already exists
        if new_username not in username_password:
            # Inform user and add new user to dictionary
            print("New user added")
            # username_password[new_username] = new_password
            # Write updated user data to file
            with open("user.txt", "w") as out_file:
                user_data = [f"{k};{username_password[k]}" for k in username_password]
                out_file.write("\n".join(user_data))
        else:
            # Inform user if username already exists
            print("Username already exists.")
    else:
        # Inform user if passwords do not match
        print("Passwords do not match.")
# Function to add a new task
def add_task():
    # Read existing tasks
    task_list = read_tasks()
    
    # Get username of person assigned to task
    task_username = input("Name of person assigned to task: ")
    
    # Check if the entered username exists
    while task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")

    # Get task details from user
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    
    # Get task due date from user and validate the format
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use YYYY-MM-DD.")
    
    # Get current date
    curr_date = date.today()
    
    # Create new task dictionary
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Add new task to task list
    task_list.append(new_task)
    
    # Write updated task list to file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            # Convert task attributes to string format
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            # Join attributes with ';' separator and append to list
            task_list_to_write.append(";".join(str_attrs))
        # Write each task entry as a line in the file
        task_file.write("\n".join(task_list_to_write))
    
    # Notify user that task has been successfully added
    print("Task successfully added.")


# Function to view all tasks
def view_all():
    task_list = read_tasks()
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine(curr_user):
    # Read the list of tasks from some source
    task_list = read_tasks()
    
    # Extract tasks assigned to the current user
    tasks_assigned_to_user = [idx + 1 for idx, t in enumerate(task_list) if t['username'] == curr_user]
    
    # If no tasks are assigned to the user, inform and return
    if not tasks_assigned_to_user:
        print("No tasks assigned to you.")
        return
    
    # Print the tasks assigned to the user with their respective numbers
    for idx, task_num in enumerate(tasks_assigned_to_user):
        print(f"{task_num}: {task_list[task_num - 1]['title']}")

    # Allow the user to select a task or return to the main menu
    while True:
        choice = input("Enter the number of the task you want to view/edit (-1 to go back to the main menu): ")
        if choice == "-1":
            return
        # Check if the choice is valid
        elif not choice.isdigit() or int(choice) not in tasks_assigned_to_user:
            print("Invalid choice. Please enter a valid task number.")
            continue
        else:
            # Get the index of the selected task
            task_idx = int(choice) - 1
            selected_task = task_list[task_idx]
            
            # Display details of the selected task
            print(f"\nTitle: {selected_task['title']}")
            print(f"Description: {selected_task['description']}")
            print(f"Due Date: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Completed: {'Yes' if selected_task['completed'] else 'No'}")

            # If the task is not completed, offer options to mark as complete or edit
            if not selected_task['completed']:
                action = input("Do you want to mark this task as complete (enter 'complete') or edit it (enter 'edit')? ").lower()
                if action == 'complete':
                    # Mark the task as complete
                    selected_task['completed'] = True
                    print("Task marked as complete.")
                    break
                elif action == 'edit':
                    # Allow the user to edit username or due date
                    edit_field = input("What do you want to edit? (username/due date): ").lower()
                    if edit_field == 'username':
                        # Update username
                        new_username = input("Enter the new username: ")
                        selected_task['username'] = new_username
                        print("Username updated successfully.")
                    elif edit_field == 'due date':
                        # Update due date with input validation
                        while True:
                            try:
                                new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                                selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                print("Due date updated successfully.")
                                break
                            except ValueError:
                                print("Invalid datetime format. Please use YYYY-MM-DD.")
                    else:
                        print("Invalid edit choice.")
                else:
                    print("Invalid action choice.")
            else:
                print("This task has already been completed and cannot be edited.")

# Function to generate reports
def generate_reports():
    # Read the list of tasks from a file
    task_list = read_tasks()
    
    # Calculate various statistics about the tasks
    num_tasks = len(task_list)
    num_completed_tasks = sum(1 for t in task_list if t['completed'])
    num_incomplete_tasks = num_tasks - num_completed_tasks
    num_overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.combine(date.today(), datetime.min.time()))

    # Count the number of users by counting non-empty lines in a file
    with open("user.txt", 'r') as user_file:
        num_users = sum(1 for line in user_file if line.strip())

    # Write task overview report to a file
    with open("task_overview.txt", 'w') as task_report_file:
        task_report_file.write(f"Total number of tasks: {num_tasks}\n")
        task_report_file.write(f"Total number of completed tasks: {num_completed_tasks}\n")
        task_report_file.write(f"Total number of uncompleted tasks: {num_incomplete_tasks}\n")
        task_report_file.write(f"Total number of tasks that are overdue: {num_overdue_tasks}\n")
        task_report_file.write(f"Percentage of tasks that are incomplete: {num_incomplete_tasks / num_tasks * 100:.2f}%\n")
        task_report_file.write(f"Percentage of tasks that are overdue: {num_overdue_tasks / num_tasks * 100:.2f}%\n")

    # Write user overview report to a file
    with open("user_overview.txt", 'w') as user_report_file:
        user_report_file.write(f"Total number of users: {num_users}\n")
        user_report_file.write(f"Total number of tasks: {num_tasks}\n")
        
        # Iterate over each user and calculate statistics
        for user, password in username_password.items():
            tasks_assigned = sum(1 for t in task_list if t['username'] == user)
            if tasks_assigned == 0:
                continue  # 
            
            tasks_completed = sum(1 for t in task_list if t['username'] == user and t['completed'])
            tasks_incomplete = tasks_assigned - tasks_completed
            tasks_overdue = sum(1 for t in task_list if t['username'] == user and not t['completed'] and t['due_date'] < datetime.combine(date.today(), datetime.min.time()))
            
            # Write user-specific statistics to the report file
            user_report_file.write(f"\nUser: {user}\n")
            user_report_file.write(f"Total number of tasks assigned: {tasks_assigned}\n")
            user_report_file.write(f"Percentage of total tasks assigned: {tasks_assigned / num_tasks * 100:.2f}%\n")
            user_report_file.write(f"Percentage of tasks completed: {tasks_completed / tasks_assigned * 100:.2f}%\n")
            user_report_file.write(f"Percentage of tasks incomplete: {tasks_incomplete / tasks_assigned * 100:.2f}%\n")
            user_report_file.write(f"Percentage of tasks overdue: {tasks_overdue / tasks_assigned * 100:.2f}%\n")

# Function to display statistics from generated reports
def display_statistics():
    # Read task overview report
    with open("task_overview.txt", 'r') as task_report_file:
        task_stats = task_report_file.read()

    # Read user overview report
    with open("user_overview.txt", 'r') as user_report_file:
        user_stats = user_report_file.read()

    # Display the statistics
    print("TASK OVERVIEW STATISTICS:")
    print(task_stats)
    print("\nUSER OVERVIEW STATISTICS:")
    print(user_stats)
# Define a boolean variable to track login status
logged_in = False

# Continue prompting for login until successful login
while not logged_in:
    # Display login prompt
    print("LOGIN")
    
    # Request username and password from user
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    
    # Check if username or password is empty, and prompt again if so
    if curr_user == "" or curr_pass == "":
        print("Username or password cannot be empty.")
        continue
    
    # Open user.txt file to read user data
    with open("user.txt", 'r') as user_file:
        # Read user data and split by newline character
        user_data = user_file.read().split("\n")
        # Create a dictionary to store username-password pairs
        username_password = {}
        # Iterate over user data and populate the dictionary
        for user in user_data:
            username, password = user.split(';')
            username_password[username] = password
    
    # Check if entered username exists in the dictionary
    if curr_user not in username_password:
        print("User does not exist.")
        continue
    # Check if entered password matches the stored password for the username
    elif username_password[curr_user] != curr_pass:
        print("Wrong password.")
        continue
    # If both username and password are correct, set login status to True and exit loop
    else:
        print("Login Successful!")
        logged_in = True

# Infinite loop to repeatedly display the menu until the user chooses to exit.
while True:
    print()  # Print a blank line for better readability.
    
    # Display the menu options and prompt the user for input.
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
g - generate report
ds - Display statistics
e - Exit
: ''').lower()  # Convert user input to lowercase for case-insensitive comparison.

    # Check the user's choice and execute the corresponding functionality.
    if menu == 'r': 
        reg_user() 
    elif menu == 'a': 
        add_task() 
    elif menu == 'va': 
        view_all() 
    elif menu == 'vm': 
        view_mine(curr_user) 
    elif menu == 'g' and curr_user == 'admin': 
        generate_reports()
        print("Reports generated successfully.")
    elif menu == 'ds': 
        display_statistics()
    elif menu == 'e': 
        print('Goodbye!!!')
        exit() 
    else: 
        print("You have made a wrong choice. Please try again.") 

