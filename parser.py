# Parser for extracting dialogue from film scripts
import sys

def main():

    filepath = sys.argv[1]
    ignore_strings = ["INT.", "EXT.", " - ", "FADE OUT", "END", ".", "CUT TO", ":"]
    film_dialogue = []

    with open(filepath, 'r') as file:
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
                    if index + 1 < len(lines):
                        dialogue_index = index + 1
                        dialogue = []
                        # Find the subsequent dialogue
                        while lines[dialogue_index].replace(" ", "") != "\n":
                            dialogue.append(lines[dialogue_index].strip())
                            if dialogue_index + 1 < len(lines):
                                dialogue_index += 1
                            else:
                                break
                        # Add it to our list of dialogue
                        film_dialogue.append(script_line + ": " + ' '.join(dialogue))

    new_filepath = filepath.replace("reduced", "parsed")

    with open(new_filepath, 'w') as file:
        for line in film_dialogue:
            file.write(line + '\n')

    print(f"Saved to {new_filepath}")

    return

if __name__ == "__main__":
    main()
