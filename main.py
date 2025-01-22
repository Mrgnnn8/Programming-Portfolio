import tkinter as tk
from tkinter import messagebox, ttk
import threading
import os
import pandas as pd
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please add it to a .env file.")

ai_client = Anthropic(api_key=API_KEY)

# File to save tasks
TASKS_FILE = "with_ai_productivity.csv"

# Global task list and conversation history
tasks = []
conversation_history = []  # Store the ongoing conversation history

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4:  # Ensure there are four parts: date, name, time, and completed
                    date, name, time, completed = parts
                    tasks.append({"date": date, "name": name, "time": time, "completed": completed})
    refresh_task_list()

def refresh_task_list():
    task_listbox.delete(0, tk.END)  # Clear the listbox
    today = datetime.now().strftime("%d/%m/%Y")  # Get today's date in the correct format
    print(f"Refreshing task list for date: {today}")  # Debugging: Log the current date

    for task in tasks:
        if task["date"] == today:  # Only display tasks for today's date
            status = "Completed" if task["completed"] == "True" else "Pending"
            display_name = f"{task['name']} - {task['time']} - {status}"
            print(f"Displaying task: {display_name}")  # Debugging: Log the task being displayed
            task_listbox.insert(tk.END, display_name)

def remove_task():
    selected = task_listbox.curselection()
    if selected:
        index_in_listbox = selected[0]  # Get the index of the selected task in the listbox
        today = datetime.now().strftime("%d/%m/%Y")  # Get today's date

        # Find the actual task in the `tasks` list based on today's date and listbox index
        filtered_tasks = [task for task in tasks if task["date"] == today]
        task_to_remove = filtered_tasks[index_in_listbox]

        # Remove the task from the original `tasks` list
        tasks.remove(task_to_remove)

        save_tasks()  # Save the updated task list to the file
        refresh_task_list()  # Refresh the listbox
    else:
        messagebox.showwarning("Error", "No task selected.")

def save_tasks():
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write(f"{task['date']},{task['name']},{task['time']},{task['completed']}\n")

def export_tasks_to_excel():
    if tasks:
        df = pd.DataFrame(tasks)
        filename = f"tasks_{datetime.now().strftime('%d-%m-%Y')}.xlsx"
        df.to_excel(filename, index=False)
        messagebox.showinfo("Export Successful", f"Tasks exported to {filename}")
    else:
        messagebox.showwarning("Error", "No tasks to export.")

def add_task(task_text=None):
    task_text = task_text or task_input.get().strip()
    if task_text:
        try:
            # Split the task text into name and time
            name, time = task_text.split(' - ')
            new_task = {
                "date": datetime.now().strftime("%d/%m/%Y"),  # Set to today's date
                "name": name.strip(),  # Ensure no extra spaces
                "time": time.strip(),  # Ensure no extra spaces
                "completed": "False"
            }
            tasks.append(new_task)
            save_tasks()
            refresh_task_list()
            task_input.delete(0, tk.END)
        except ValueError:
            # If the input doesn't follow "Task Name - Time" format, show an error
            messagebox.showwarning("Error", "Task must be in the format: 'Task Name - Time'")
    else:
        messagebox.showwarning("Error", "Task cannot be empty.")

def complete_task():
    selected = task_listbox.curselection()
    if selected:
        index_in_listbox = selected[0]
        today = datetime.now().strftime("%d/%m/%Y")  # Get today's date

        # Find the actual task in the `tasks` list based on today's date and listbox index
        filtered_tasks = [task for task in tasks if task["date"] == today]
        task_to_complete = filtered_tasks[index_in_listbox]

        # Mark the task as completed in the original `tasks` list
        for task in tasks:
            if task == task_to_complete:
                task["completed"] = "True"  # Update the 'completed' status

        save_tasks()  # Save the updated task list to the file
        refresh_task_list()  # Refresh the listbox
    else:
        messagebox.showwarning("Error", "No task selected.")

def handle_ai_response(user_input):
    global conversation_history

    # Add the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = ai_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.5,
            system="You are a productivity assistant helping with tasks and queries.",
            messages=[
                {"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}]}
                for msg in conversation_history
            ],
        )

        # Extract Claude's response and add it to the history
        assistant_reply = "\n".join(block.text for block in response.content if hasattr(block, "text"))
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        return f"Error: {e}"

def send_message():
    user_input = chat_input.get().strip()
    if not user_input:
        messagebox.showwarning("Error", "Please enter a message.")
        return

    # Display the user's message
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_input}\n")
    chat_display.config(state=tk.DISABLED)

    chat_input.delete(0, tk.END)

    # Get Claude's response
    threading.Thread(target=generate_ai_response, args=(user_input,)).start()

def generate_ai_response(user_input):
    response = handle_ai_response(user_input)
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Assistant: {response}\n\n")
    chat_display.config(state=tk.DISABLED)

def add_from_chat():
    try:
        selected_text = chat_display.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        if selected_text:
            add_task(selected_text)
    except tk.TclError:
        messagebox.showwarning("Error", "Please select some text from the chat first.")

def clear_conversation():
    global conversation_history
    conversation_history = []
    chat_display.config(state=tk.NORMAL)
    chat_display.delete(1.0, tk.END)
    chat_display.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Productivity Assistant")
root.geometry("900x700")
root.config(bg="#2C2F33")

header = tk.Label(root, text="Daily Productivity Assistant", font=("Segoe UI", 18, "bold"), bg="#7289DA", fg="white", pady=10)
header.pack(fill=tk.X)

chat_frame = tk.Frame(root, bg="#2C2F33")
chat_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
chat_display = tk.Text(chat_frame, wrap="word", state="disabled", bg="#23272A", fg="#F0F0F0", font=("Segoe UI", 12), bd=0, padx=10, pady=10)
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_scroll = tk.Scrollbar(chat_frame, command=chat_display.yview, bg="#2C2F33")
chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)
chat_display["yscrollcommand"] = chat_scroll.set

chat_input_frame = tk.Frame(root, bg="#2C2F33")
chat_input_frame.pack(padx=20, pady=5, fill=tk.X)
chat_input = tk.Entry(chat_input_frame, font=("Segoe UI", 12), bg="#23272A", fg="#F0F0F0", bd=1, relief="flat")
chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
send_button = ttk.Button(chat_input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

clear_button = ttk.Button(chat_input_frame, text="New Chat", command=clear_conversation)
clear_button.pack(side=tk.LEFT, padx=5)

task_frame = tk.Frame(root, bg="#2C2F33")
task_frame.pack(padx=20, pady=10, fill=tk.BOTH)
task_label = tk.Label(task_frame, text="Daily Planner", font=("Segoe UI", 14, "bold"), bg="#2C2F33", fg="#F0F0F0")
task_label.pack(anchor="w", padx=10)
task_listbox = tk.Listbox(task_frame, font=("Segoe UI", 12), bg="#23272A", fg="#F0F0F0", selectbackground="#7289DA", selectforeground="white", bd=0, relief="flat")
task_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

task_control_frame = tk.Frame(root, bg="#2C2F33")
task_control_frame.pack(padx=20, pady=10, fill=tk.X)
task_input = tk.Entry(task_control_frame, font=("Segoe UI", 12), bg="#23272A", fg="#F0F0F0", bd=1, relief="flat")
task_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
add_task_button = ttk.Button(task_control_frame, text="Add", command=add_task)
add_task_button.pack(side=tk.LEFT, padx=5)
complete_task_button = ttk.Button(task_control_frame, text="Complete", command=complete_task)
complete_task_button.pack(side=tk.LEFT, padx=5)
remove_task_button = ttk.Button(task_control_frame, text="Remove", command=remove_task)
remove_task_button.pack(side=tk.LEFT, padx=5)
export_button = ttk.Button(task_control_frame, text="Export Tasks", command=export_tasks_to_excel)
export_button.pack(side=tk.RIGHT, padx=10)

footer = tk.Label(root, text="Designed by Morgan Jones", font=("Segoe UI", 10), bg="#2C2F33", fg="#7289DA", pady=5)
footer.pack(fill=tk.X)

root.after(100, load_tasks)
root.mainloop()

