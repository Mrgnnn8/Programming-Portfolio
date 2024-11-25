# Import required libraries
import os
import json
import logging
import threading
import time
import tkinter as tk
from tkinter import messagebox, filedialog
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Raise an error if the API key is not found
if not API_KEY:
    raise ValueError("API key not found. Please set it in a .env file.")

# Configure logging to save application events in a log file
logging.basicConfig(
    filename="chat_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create an Anthropic API client using the API key
client = Anthropic(api_key=API_KEY)

# Initialize chat history as an empty list
chat_history = []

# Function to send a request to the Anthropic API and get a response
def get_response(prompt: str, model: str, max_tokens: int, temperature: float, retries: int = 3) -> str:
    for attempt in range(1, retries + 1):
        try:
            # Send the request to the API
            message = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system="You are a direct, fact-based assistant. Answer questions concisely without additional pleasantries.",
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            )
            # Extract the response text from the API response
            if hasattr(message, "content") and isinstance(message.content, list):
                return "\n".join(block.text for block in message.content if hasattr(block, "text"))
            return message.content
        except Exception as e:
            # Log and handle errors, with retry logic for server overload
            error_message = str(e)
            print(f"Attempt {attempt}: {error_message}")
            if "overloaded" in error_message.lower():
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return f"Error: {e}"
    return "Error: Claude servers are currently overloaded. Please try again later."

# Function to save chat history to a JSON file
def save_chat_history(history, filename="chat_history.json"):
    try:
        with open(filename, "w") as file:
            json.dump(history, file, indent=4)
        logging.info("Chat history saved successfully.")
        messagebox.showinfo("Save Chat", "Chat history saved successfully.")
    except Exception as e:
        # Handle errors during the save operation
        logging.error(f"Error while saving chat history: {e}")
        messagebox.showerror("Save Chat", f"Error while saving chat history: {e}")

# Function to load chat history from a JSON file
def load_chat_history(filename="chat_history.json"):
    global chat_history
    try:
        if os.path.exists(filename):
            # Load the chat history from the file
            with open(filename, "r") as file:
                chat_history = json.load(file)
            logging.info("Chat history loaded successfully.")
            display_chat_history()  # Display the loaded chat history in the chat window
            messagebox.showinfo("Load Chat", "Chat history loaded successfully.")
        else:
            # Handle the case where the file does not exist
            logging.warning("Chat history file not found. Starting a new history.")
            messagebox.showwarning("Load Chat", "Chat history file not found. Starting a new history.")
    except Exception as e:
        # Handle errors during the load operation
        logging.error(f"Error while loading chat history: {e}")
        messagebox.showerror("Load Chat", f"Error while loading chat history: {e}")

# Function to display the chat history in the chat window
def display_chat_history():
    chat_display.config(state=tk.NORMAL)
    chat_display.delete(1.0, tk.END)
    for entry in chat_history:
        # Display user and assistant messages
        chat_display.insert(tk.END, f"You: {entry['user']}\n", 'user')
        chat_display.insert(tk.END, f"Claude: {entry['claude']}\n\n", 'claude')
    chat_display.config(state=tk.DISABLED)

# Function to handle sending user messages
def send_message():
    user_input = input_field.get().strip()  # Get user input
    if user_input == "":
        # Warn if the input is empty
        messagebox.showwarning("Input Error", "Please enter a message.")
        return

    send_button.config(state=tk.DISABLED)  # Disable send button while processing

    # Display the user's message in the chat window
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_input}\n", 'user')
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

    input_field.delete(0, tk.END)  # Clear the input field

    logging.info(f"User: {user_input}")

    chat_history.append({"user": user_input, "claude": ""})  # Add to chat history

    # Handle the response in a separate thread
    threading.Thread(target=handle_response, args=(user_input,)).start()

# Function to handle the response from the API
def handle_response(user_input):
    model = "claude-3-5-sonnet-20241022"  # Specify the model
    max_tokens = 1000  # Maximum tokens for the response
    temperature = 0.5  # Temperature for response variability

    response = get_response(
        prompt=user_input,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )

    # Update the last chat history entry with the assistant's response
    if chat_history:
        chat_history[-1]["claude"] = response

    # Update the chat display with the response
    root.after(0, lambda: update_chat_display(response))

# Function to update the chat display with the assistant's response
def update_chat_display(response):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Claude: {response}\n\n", 'claude')
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

    logging.info(f"Claude: {response}")

    if response.startswith("Error:"):
        # Show an error message if the response contains an error
        messagebox.showerror("API Error", response)

    send_button.config(state=tk.NORMAL)  # Re-enable send button

# Function to save chat history using a file dialog
def save_chat():
    filename = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if filename:
        save_chat_history(chat_history, filename)

# Function to load chat history using a file dialog
def load_chat():
    filename = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if filename:
        load_chat_history(filename)

# Create the main application window
root = tk.Tk()
root.title("Claude Chat Application")
root.geometry("700x600")
root.resizable(False, False)

# Configure the grid layout for the main window
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)

# Main frame to hold chat and input sections
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

# Chat frame to display chat messages
chat_frame = tk.Frame(main_frame)
chat_frame.grid(row=0, column=0, sticky="nsew")

# Text widget to display chat messages
chat_display = tk.Text(
    chat_frame,
    wrap='word',
    state=tk.DISABLED,
    bg="#FFFFFF",
    fg="#000000",
    font=("Helvetica", 12)
)
chat_display.grid(row=0, column=0, sticky="nsew")

chat_frame.columnconfigure(0, weight=1)
chat_frame.rowconfigure(0, weight=1)

# Scrollbar for the chat display
scrollbar = tk.Scrollbar(chat_frame, command=chat_display.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
chat_display['yscrollcommand'] = scrollbar.set

# Configure text tags for styling user and assistant messages
chat_display.tag_config('user', foreground='black', font=("Helvetica", 12, "bold"))
chat_display.tag_config('claude', foreground='black', font=("Helvetica", 12, "bold"))

# Input frame to hold the input field and buttons
input_frame = tk.Frame(root, bd=2, relief='sunken')
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
input_frame.columnconfigure(0, weight=1)

# Entry widget for user input
input_field = tk.Entry(input_frame, font=("Helvetica", 12))
input_field.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")
input_field.focus_set()

# Bind Enter key to the send_message function
input_field.bind("<Return>", lambda event: send_message())

# Button to send user messages
send_button = tk.Button(
    input_frame,
    text="Send",
    width=10,
    command=send_message,
    font=("Helvetica", 12)
)
send_button.grid(row=0, column=1, padx=(0, 5))

# Button to save chat history
save_button = tk.Button(
    input_frame,
    text="Save Chat",
    width=10,
    command=save_chat,
    font=("Helvetica", 12)
)
save_button.grid(row=0, column=2, padx=(0, 5))

# Button to load chat history
load_button = tk.Button(
    input_frame,
    text="Load Chat",
    width=10,
    command=load_chat,
    font=("Helvetica", 12)
)
load_button.grid(row=0, column=3, padx=(0, 5))

# Button to exit the application
exit_button = tk.Button(
    input_frame,
    text="Exit",
    width=10,
    command=root.quit,
    font=("Helvetica", 12)
)
exit_button.grid(row=0, column=4, padx=(0, 5))

# Start the Tkinter event loop
root.mainloop()


