import musicxml_engine as musicxml
import script_builder
import os

converter = musicxml.convert_musicxml_to_standard_notation


def setup():
    config_file = open("config.txt", "w")
    root_path = input("Enter the root path of your music folders: ")
    config_file.write(f"ROOT_PATH={root_path}\n")

    config_file.close()


def main_menu(music_dict):
    print("Select a music to start conversion:")
    for i, key in enumerate(music_dict.keys()):
        print(f"{i + 1} - {key}")
    selection = int(input(">"))
    os.system("cls" if os.name == "nt" else "clear")

    if selection not in range(len(music_dict.keys()) + 1):
        print("Invalid selection")
        main_menu(music_dict)
    elif selection <= 0:
        print("Invalid selection")
        main_menu(music_dict)
    else:
        print(f"Selected {selection}")
        return list(music_dict.keys())[selection - 1]


def action_menu():
    print("Want to build the arduino script? (y/n)")
    selection = input(">")
    if selection == "y":
        print("Type the arduino buzzer pin:")
        selection = input(">")
        try:
            selection = int(selection)
        except ValueError:
            print("Invalid selection")
            os.system("cls" if os.name == "nt" else "clear")
            action_menu()
        else:
            return True, selection
    elif selection == "n":
        return False, -1
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("Invalid selection")
        action_menu()


def get_music_xml_files(path):
    music_xml_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".musicxml"):
                music_xml_files.append(os.path.join(root, file))
    return music_xml_files


def get_music_folders(path):
    music_folders = []
    for root, dirs, _ in os.walk(path):
        for dir in dirs:
            music_folders.append(os.path.join(dir))
    return music_folders


configs = {}
root_path = ""

# * Integrity checks:
if not os.path.exists("output"):
    os.mkdir("output")

if not os.path.exists("config.txt"):
    setup()
# * End of integrity checks

with open("config.txt", "r") as file:
    for line in file.readlines():
        if line.startswith("#"):
            continue
        key, value = line.split("=")
        configs[key] = value.strip()

try:
    root_path = configs["ROOT_PATH"]
except KeyError:
    print("Error: ROOT_PATH not found in config.txt")
    setup()

music = {}

music_folders = get_music_folders(root_path)

for folder in music_folders:
    music[folder] = get_music_xml_files(os.path.join(root_path, folder))

music_to_be_converted = main_menu(music)
build, buzzer_pin = action_menu()  # type: ignore

# The melodies already converted to arduino code will be stored here
ardu_melodies: list[str] = []
melodies_tempo: list[int] = []
music_names: list[str] = []


for xml_file_path in music[music_to_be_converted]:

    music_names.append(xml_file_path.split("\\")[-1].split(".")[0])

    with open(xml_file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    # Using the imported function from musicxml_engine.py
    notes, durations, tempo = converter(xml_content)
    melody: str = ""
    melodies_tempo.append(tempo)

    # TODO: refactor: modularize this (unessary code repetition)
    if not build:
        print(f"Converted {xml_file_path}\n")
    for note, duration in zip(notes, durations):
        if note == "REST":
            melody += f", REST, {duration}"
            if not build:
                print(f", REST, {duration}", end="")
        else:
            melody += f", NOTE_{note}, {duration}"
            if not build:
                print(f", NOTE_{note}, {duration}", end="")

    #  Removing the first trailing comma and space
    melody = melody[2:]
    ardu_melodies.append(melody)
    print("\n")

if build:
    for name, melody, tempo in zip(music_names, ardu_melodies, melodies_tempo):  # type: ignore

        # ! Hardcoded, needs to be changed
        script_builder.build_arduino_script(tempo, melody, 11, name)  # type: ignore
    print("Scripts built into ./output folder")

