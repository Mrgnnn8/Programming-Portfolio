with open("Input/Letters/starting_letter.txt", "r") as letter_file:
    first = letter_file.read() 

with open("Input/Names/invited_names.txt", "r") as names_file:
    names = names_file.readlines() 

for name in names:
    stripped_name = name.strip() 
    personalized_letter = first.replace("[name]", stripped_name)  

    with open(f"Output/ReadyToSend/letter_for_{stripped_name}.txt", "w") as output_file:
        output_file.write(personalized_letter)
