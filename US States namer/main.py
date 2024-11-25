import turtle
import pandas

# Set up the screen and add the map image
screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

# Load the data from the CSV file
data = pandas.read_csv("50_states.csv")
all_states = data.state.to_list()  # Convert the 'state' column to a list for easy comparison
guessed_states = []  # List to track correctly guessed states

# Main game loop
while len(guessed_states) < 50:  # Continue until all 50 states are guessed
    # Prompt the user to input a state name
    answer_state = screen.textinput(
        title=f"{len(guessed_states)}/50 States Correct",
        prompt="What's another state's name?"
    ).title()  # Capitalize the first letter of each word for consistency

    # Exit the game if the user types 'Exit'
    if answer_state == "Exit":
        # Create a list of states that were not guessed
        missing_states = [state for state in all_states if state not in guessed_states]
        
        # Save the missing states to a CSV file for learning purposes
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break

    # Check if the guessed state is correct
    if answer_state in all_states and answer_state not in guessed_states:
        guessed_states.append(answer_state)  # Add the correct guess to the list
        
        # Create a turtle to write the state name on the map
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        
        # Get the state's coordinates from the data
        state_data = data[data.state == answer_state]
        t.goto(state_data.x.item(), state_data.y.item())  # Move to the state's location
        t.write(answer_state)  # Write the state name on the map

