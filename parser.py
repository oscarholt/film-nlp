# Parser for extracting dialogue from film scripts
import sys

def main():

    ignore_strings = ["INT.", "EXT.", " - ", "FADE OUT", "END"]

    film_dialogue = []

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

        for index, line in enumerate(lines):
            # Strip whitespace and newline from our line
            script_line = line.strip()
            # Determine whether the line is a character line
            if script_line == script_line.upper():
                character_line = True

                for string in ignore_strings:
                    if string in script_line:
                        character_line = False

                if len(script_line) == 0:
                    character_line = False

                # Now we assume it's a character line
                if character_line:
                    dialogue_index = index + 1
                    dialogue = []
                    # Find the subsequent dialogue
                    while lines[dialogue_index].replace(" ", "") != "\n":
                        dialogue.append(lines[dialogue_index].strip())
                        dialogue_index += 1
                    # Add it to our list of dialogue
                    film_dialogue.append(script_line + ": " + ' '.join(dialogue))

    for line in film_dialogue:
        print(line)

    return True

if __name__ == "__main__":
    main()
