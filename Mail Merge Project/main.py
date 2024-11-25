# Open the starting letter template file in read mode
with open("Input/Letters/starting_letter.txt", "r") as letter_file:
    first = letter_file.read()  # Read the entire content of the letter template into a variable

# Open the invited names file in read mode
with open("Input/Names/invited_names.txt", "r") as names_file:
    names = names_file.readlines()  # Read all lines (names) from the file into a list

# Loop through each name in the list of names
for name in names:
    stripped_name = name.strip()  # Remove any leading or trailing whitespace characters
    # Replace the placeholder [name] in the template with the actual name
    personalized_letter = first.replace("[name]", stripped_name)  

    # Create a new personalized letter file for the current name
    with open(f"Output/ReadyToSend/letter_for_{stripped_name}.txt", "w") as output_file:
        output_file.write(personalized_letter)  # Write the personalized letter content to the file
