import time
import os
import keyboard
import shutil


def lijst_boeken():
    # Krijg een lijst van alle bestanden in de huidige directory
    alle_bestanden = os.listdir()

    # Filter alleen de .txt-bestanden uit de lijst
    alle_txt_bestanden = [bestand for bestand in alle_bestanden if bestand.endswith('.txt')]
    # Print de resulterende lijst
    for item in alle_txt_bestanden:
        #haal de extentie .txt van het item zodat je alleen de boeknamen overhoudt
        boek = os.path.splitext(item)[0]
        print(boek)



def kies_boek():
    print()
    print('Dit is een tekstlezer voor je computer')
    print('Je krijgt een lijst te zien van boeken die je kunt lezen')
    print('Als je zelf een tekst(.txt) bestand hebt kun je het er bij zetten')
    print('Als je klaar bent druk je op q het programma onthoudt waar je gebleven bent')
    print()
    boek1 = input('Kies een boek uit de lijst:\n')
    boek=boek1+'.txt'
    return boek


# het schoonmaken van het scherm en bepalen waar je opnieuw begint met het aantal lines_before=
def clear_screen(lines_before=10):
    # kijk welk besturingssysteem er is en maak het scherm schoon
    if os.name == 'nt':  # 'nt' staat voor Windows
        os.system('cls')
    else:
        os.system('clear')

    # voeg lege regels toe aan het begin
    for _ in range(lines_before):
        print()


# hier wordt de text weergegeven met vertraging die je verderop kunt instellen
def type_like_chatgpt(text, delay):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


# opent het bestand en leest de regels en zorgt dat het doorgaat als het een onbekent teken tegenkomt in het bestand
def read_text_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f'Bestand "{file_path}" niet gevonden.')
        return []


# Functie om de huidige positie op te slaan naar een bestand
def save_position(file_path, current_line):
    with open(file_path + ".position", 'w') as position_file:
        position_file.write(str(current_line))


# Functie om de opgeslagen positie uit het bestand te lezen
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

    # Voeg de laatste regel toe
    wrapped_lines.append(current_line.strip())

    return '\n'.join(wrapped_lines)


def display_line_with_wrap(line, delay, line_width):
    words = line.strip().split()

    try:
        # Probeer de woorden van de huidige zin op een nieuwe regel te wikkelen
        wrapped_line = wordWrap(words, line_width)
    except TypeError:
        pass

    # Print de regels met vertraging
    if isinstance(wrapped_line, str):
        type_like_chatgpt(wrapped_line, delay)


def main():
    lijst_boeken()
    gekozen_boek = kies_boek()
    file_path = gekozen_boek
    current_line = load_position(file_path)
    print(f"Current line: {current_line}")  # Controleer de huidige positie
    lines = read_text_file(file_path)
    print(f"Number of lines: {len(lines)}")  # Controleer het aantal regels in het bestand
    delay_factor = 0.05
    line_width = shutil.get_terminal_size().columns  # Dynamisch ophalen van de terminalbreedte
    print(f"Terminal width: {line_width}")  # Controleer de terminalbreedte

    try:
        for line in lines[current_line:]:
            clear_screen()
            display_line_with_wrap(line, delay_factor, line_width)
            #print(f"Displaying line: {line}")  # Controleer de huidige regel die wordt weergegeven
            # Wacht op toetsaanslagen zonder Enter
            event = keyboard.read_event(suppress=True)
            #print(f"Event: {event}")  # Controleer het toetsenbordgebeurtenisobject
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'up':
                    delay_factor -= 0.01
                elif event.name == 'down':
                    delay_factor += 0.01
                elif event.name == 'q':
                    print()
                    print()
                    print('    het programma wordt afgesloten...')
                    break
                delay_factor = max(0.01, min(delay_factor, 1.0))
            current_line += 1  # Verhoog de huidige positie
            #print(f"Updated current line: {current_line}")  # Controleer de bijgewerkte positie
    except keyboard.KeyboardEvent:
        pass

    save_position(file_path, current_line)
    #print(f"Position saved: {current_line}")  # Controleer of de positie correct is opgeslagen


if __name__ == "__main__":
    main()