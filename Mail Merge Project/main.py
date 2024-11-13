# Open the starting letter template
with open("Input/Letters/starting_letter.txt", "r") as letter_file:
    first = letter_file.read()  # Read the whole letter template

# Open the list of invited names
with open("Input/Names/invited_names.txt", "r") as names_file:
    names = names_file.readlines()  # Read all names

# For each name, create a personalized letter
for name in names:
    stripped_name = name.strip()  # Remove newline characters from the name
    personalized_letter = first.replace("[name]", stripped_name)  # Replace [name] with the actual name

    # Write the personalized letter to a new file
    with open(f"Output/ReadyToSend/letter_for_{stripped_name}.txt", "w") as output_file:
        output_file.write(personalized_letter)
