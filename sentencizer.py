import time
import os
import keyboard
import shutil


def lijst_boeken():
    # Get a list of all files in the current directory
    alle_bestanden = os.listdir()

    # Filter out only the .txt files from the list
    alle_txt_bestanden = [bestand for bestand in alle_bestanden if bestand.endswith('.txt')]
    # Print the resulting list
    for item in alle_txt_bestanden:
        # Remove the .txt extension from the item so that only the book names remain
        boek = os.path.splitext(item)[0]
        print(boek)


def kies_boek():
    print()
    print('This is a text reader for your computer')
    print('You will see a list of books that you can read')
    print('If you have your own text (.txt) file, you can add it')
    print('When you are done, press q, the program will remember where you left off')
    print()
    boek1 = input('Choose a book from the list:\n')
    boek = boek1 + '.txt'
    return boek


# Clearing the screen and determining where to start again with the number of lines_before=
def clear_screen(lines_before=10):
    # Check which operating system is being used and clear the screen
    if os.name == 'nt':  # 'nt' stands for Windows
        os.system('cls')
    else:
        os.system('clear')

    # Add empty lines at the beginning
    for _ in range(lines_before):
        print()


# Here the text is displayed with a delay that you can set later
def type_like_chatgpt(text, delay):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


# Opens the file and reads the lines, and ensures it continues if it encounters an unknown character in the file
def read_text_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f'File "{file_path}" not found.')
        return []


# Function to save the current position to a file
def save_position(file_path, current_line):
    with open(file_path + ".position", 'w') as position_file:
        position_file.write(str(current_line))


# Function to read the saved position from the file
def load_position(file_path):
    try:
        with open(file_path + ".position", 'r') as position_file:
            return int(position_file.read())
    except FileNotFoundError:
        return 0


def wordWrap(words, lineWidth):
    wrapped_lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) > lineWidth:
            wrapped_lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line += word + " "

    # Add the last line
    wrapped_lines.append(current_line.strip())

    return '\n'.join(wrapped_lines)


def display_line_with_wrap(line, delay, line_width):
    words = line.strip().split()

    try:
        # Try to wrap the words of the current sentence onto a new line
        wrapped_line = wordWrap(words, line_width)
    except TypeError:
        pass

    # Print the lines with a delay
    if isinstance(wrapped_line, str):
        type_like_chatgpt(wrapped_line, delay)


def main():
    lijst_boeken()
    gekozen_boek = kies_boek()
    file_path = gekozen_boek
    current_line = load_position(file_path)
    print(f"Current line: {current_line}")  # Check the current position
    lines = read_text_file(file_path)
    print(f"Number of lines: {len(lines)}")  # Check the number of lines in the file
    delay_factor = 0.05
    line_width = shutil.get_terminal_size().columns  # Dynamically get the terminal width
    print(f"Terminal width: {line_width}")  # Check the terminal width

    try:
        for line in lines[current_line:]:
            clear_screen()
            display_line_with_wrap(line, delay_factor, line_width)
            #print(f"Displaying line: {line}")  # Check the current line being displayed
            # Wait for keystrokes without pressing Enter
            event = keyboard.read_event(suppress=True)
            #print(f"Event: {event}")  # Check the keyboard event object
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'up':
                    delay_factor -= 0.01
                elif event.name == 'down':
                    delay_factor += 0.01
                elif event.name == 'q':
                    print()
                    print()
                    print('    The program is closing...')
                    break
                delay_factor = max(0.01, min(delay_factor, 1.0))
            current_line += 1  # Increment the current position
            #print(f"Updated current line: {current_line}")  # Check the updated position
    except keyboard.KeyboardEvent:
        pass

    save_position(file_path, current_line)
    #print(f"Position saved: {current_line}")  # Check if the position was saved correctly


if __name__ == "__main__":
    main()
