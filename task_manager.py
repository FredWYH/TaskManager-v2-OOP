#!/usr/bin/env python3

import datetime
import os

def login():
	while True:
		username = input("Enter your username: ")
		password = input("Enter your password: ")
		with open("user.txt", "r") as f:
			for line in f:
				if line.strip() == f"{username}, {password}":
					return username
		print("Invalid username or password. Please try again.")
		
def reg_user():
	# Check if the user trying to register is 'admin'
	if username != 'admin':
		print("Only the 'admin' user can register new users.")
		return
	
	# Read the contents of the user.txt file
	with open('user.txt', 'r') as file:
		users = file.readlines()
	# Iterate through the list of users and check if the new username already exists
	new_username = input("Enter the new username: ")
	for user in users:
		if new_username in user:
			print("A user with that username already exists.")
			return
	# If the username does not exist, prompt for password and confirmation
	new_password = input("Enter the new password: ")
	confirm_password = input("Confirm the password: ")
	if new_password == confirm_password:
		# Write the new username and password to the user.txt file
		with open('user.txt', 'a') as file:
			file.write(f"{new_username}, {new_password}\n")
		print(f"New user {new_username} has been added.")
	else:
		print("Passwords do not match.")
		
def add_task():
	assigned_to = input("Enter the username of the person the task is assigned to: ")
	title = input("Enter the title of the task: ")
	description = input("Enter a description of the task: ")
	due_date = input("Enter the due date of the task (DD-MMM-YYYY): ")
	date_assigned = datetime.datetime.now().strftime("%d-%b-%Y")
	with open("tasks.txt", "a") as f:
		f.write(f"{assigned_to}, {title}, {description}, {date_assigned}, {due_date}, No\n")
	print("Task added.")
	
def view_all():
	with open("tasks.txt", "r") as f:
		for line in f:
			print(line.strip())
			
def view_mine(username):
	tasks = read_tasks()
	my_tasks = [task for task in tasks if task[0] == username]
	if not my_tasks:
		print("You have no tasks assigned to you.")
		return
	for i, task in enumerate(my_tasks):
		print(f"{i+1}. {task[1]} - Due on {task[4]}")
	while True:
		choice = input("Enter the number of the task you want to view or -1 to return to main menu: ")
		if choice == "-1":
			return
		try:
			task_index = int(choice) - 1
			if task_index < 0 or task_index >= len(my_tasks):
				raise ValueError
			task = my_tasks[task_index]
			print(f"Task: {task[1]}\nAssigned to: {task[0]}\nDescription: {task[2]}\nDue date: {task[4]}")
			if task[5] == 'Yes':
				print("This task is completed.")
				continue
			while True:
				action = input("What would you like to do? (c)omplete, (e)dit or (r)eturn to main menu: ")
				if action == 'c':
					task[5] = 'Yes'
					write_tasks(tasks)
					print("Task completed.")
					break
				elif action == 'e':
					task[0] = input("Enter the new username to assign the task: ")
					task[4] = input("Enter the new due date for the task: ")
					write_tasks(tasks)
					print("Task edited.")
					break
				elif action == 'r':
					break
				else:
					print("Invalid choice.")
		except ValueError:
			print("Invalid choice.")

def generate_report():
	#check if file exist, if not, create file.
	if os.path.exists('task_overview.txt') == False:
		task = open('task_overview.txt', 'x')
		task.close()
	#read task file
	tasks_list = []
	with open('tasks.txt', 'r+') as file_tasks:
		for line in file_tasks:
			l_tidy = line.strip('\n').split(",")
			tasks_list.append([l.strip() for l in l_tidy])
			
	# Get the total number of tasks
	total_tasks = len(tasks_list)
	
	# Get the number of completed tasks
	completed_tasks = 0
	for tasks in tasks_list:
		if tasks[5] == "Yes":
			completed_tasks += 1
			
	# Get the number of uncompleted tasks
	uncompleted_tasks = total_tasks - completed_tasks
	
	# Get the number of overdue tasks
	overdue_tasks = 0
	for tasks in tasks_list:
		if tasks[5] == "No" and tasks[4] <= str(datetime.now()):
			overdue_tasks += 1
	# Calculate the percentage of tasks that are incomplete
	incomplete_percent = (uncompleted_tasks / total_tasks) * 100
	
	# Calculate the percentage of tasks that are overdue
	overdue_percent = (overdue_tasks / total_tasks) * 100
	
	# Create the task_overview.txt file and write the data
	with open("task_overview.txt", "w") as file:
		file.write("Total number of tasks: {}\n".format(total_tasks))
		file.write("Total number of completed tasks: {}\n".format(completed_tasks))
		file.write("Total number of uncompleted tasks: {}\n".format(uncompleted_tasks))
		file.write("Total number of overdue tasks: {}\n".format(overdue_tasks))
		file.write("Percentage of tasks that are incomplete: {:.2f}%\n".format(incomplete_percent))
		file.write("Percentage of tasks that are overdue: {:.2f}%\n".format(overdue_percent))
	print("task_overview.txt file has been generated.")

	#check if file exist, if not, create file.
	if os.path.exists('user_overview.txt') == False:
		userFile = open('user_overview.txt', 'x')
		userFile.close()
	#read user file
	users_list = []
	with open('user.txt', 'r+') as file_users:
		for line in file_users:
			l_tidy = line.strip('\n').split(",")
			users_list.append([l.strip() for l in l_tidy])
			
	# Get the total number of users
	total_users = len(users_list)
	
	# Create the user_overview.txt file and write the data
	with open("user_overview.txt", "w") as file:
		file.write("Total number of users: {}\n".format(total_users))
		file.write("Total number of tasks: {}\n".format(total_tasks))
		
		for user in users_list:
			user_tasks = [task for task in tasks_list if task[0] == username]
			
			total_user_tasks = len(user_tasks)
			
			completed_user_tasks = len([task for task in user_tasks if task[5] == "Yes"])
			uncompleted_user_tasks = total_user_tasks - completed_user_tasks
			overdued_user_tasks = len([task for task in user_tasks if task[5] == "No" and task[4] < str(datetime.now())])
			
			# Calculate the percentage of total tasks assigned to the user
			percent_total_tasks_assigned = (total_user_tasks / total_tasks) * 100
			
			# Calculate the percentage of tasks assigned to the user that have been completed
			percent_completed_user_tasks = (completed_user_tasks / total_user_tasks) * 100
			
			# Calculate the percentage of tasks assigned to the user that have to be completed
			percent_uncompleted_user_tasks = (uncompleted_user_tasks / total_user_tasks) * 100
			
			# Calculate the percentage of tasks assigned to the user that are overdue
			percent_overdued_user_tasks = (overdued_user_tasks / total_user_tasks) * 100
			
			file.write(f"Total number of task for {username}: {total_user_tasks}\n")
			file.write(f"Total percentage of tasks for {username}: {percent_total_tasks_assigned}%\n")
			file.write(f"Total percentage of completed tasks for {username}: {percent_completed_user_tasks}%\n")
			file.write(f"Total percentage of uncompleted tasks for {username}: {percent_uncompleted_user_tasks}%\n")
			file.write(f"Total percentage of overdued tasks for {username}: {percent_overdued_user_tasks}%\n")
		print("user_overview.txt file has been generated.")
			
			
def display_stats():
	if login() != "admin":
		print("Only the admin user can access the statistics.")
		return
	# Check if the report files exist, if not generate them
		if not (os.path.exists("task_overview.txt") and os.path.exists("user_overview.txt")):
			generate_report()
			
		# Open and read the task_overview.txt file
		with open("task_overview.txt", "r") as file:
			task_data = file.read()
		print("Task Overview:\n", task_data)
	
		# Open and read the user_overview.txt file
		with open("user_overview.txt", "r") as file:
			user_data = file.read()
		print("User Overview:\n", user_data)
	
	
def main():
	while True:
		username = login()
		if username:
			while True:
				print("""
					(r) Register user (admin only)
					(a) Add task
					(va) View all tasks
					(vm) View my tasks
					(gr) Generate report
					(ds) Display statistics (admin only)
					(q) Quit
					""")
				choice = input("Enter choice: ").lower()
				if choice == "q":
					break
				elif choice == "r":
						reg_user(username)
				elif choice == "a":
						add_task(username)
				elif choice == "va":
						view_all()
				elif choice == "vm":
						view_mine(username)
				elif choice == "gr":
						generate_report()
				elif choice == "ds":
						display_stats()
				else:
					print("You have enter an invalid choice")
					
if __name__ == "__main__":
	main()