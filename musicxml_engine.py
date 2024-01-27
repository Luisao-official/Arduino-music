import xml.etree.ElementTree as ET


def convert_musicxml_to_standard_notation(xml_data):
    root = ET.fromstring(xml_data)

    divisions = int(root.find(".//divisions").text)

    # Getting main attributes

    tempo = int(float(root.find('.//sound').get('tempo')))
    # key_fifths = int(root.find('.//key/fifths').text)

    # Time signature
    # Time beats is the number of beats per measure

    time_beats = int(root.find('.//time/beats').text)
    # Time beat type is the type of note that gets the beat
    beat_type = int(root.find('.//time/beat-type').text)

    # Key signature
    # clef_sign = root.find('.//clef/sign').text
    # clef_line = int(root.find('.//clef/line').text)

    notes_list = []
    durations_list = []

    for measure in root.findall(".//measure"):
        for note_elem in measure.findall(".//note"):
            is_dotted = False
            duration = int(note_elem.find("duration").text)
            if not duration:
                # Avoiding division by zero
                continue
            # print(f"Durration {duration}")
            is_rest = note_elem.find("rest") is not None

            # print(f"Divisions {divisions}")

            # ? let y be time_beats and x be beat_type:
            # The fraction of a whole note that this note represents and is based on a 4/x measure
            # so to convert it to the y/x measure we need to multiply it by y/4
            calculated_duration = duration / divisions * time_beats / 4

            if is_rest and calculated_duration < 0.005:
                # skippable rest
                continue

            elif calculated_duration < 1:
                calculated_duration = duration / divisions
                # print(f"Calculated duration {calculated_duration}")

                # Calculate the inverse to check if it's close to a dotted note
                inverse_duration = 1 / calculated_duration
                # print(f"Inverse duration {inverse_duration}")

                calculated_duration = round(beat_type * inverse_duration)
                # print(f"Calculated smaller note duration {calculated_duration}")

            elif calculated_duration > 1:
                # calculated_duration /= 4
                # print(f"Calculated bigger note duration {calculated_duration}")
                calculated_duration = round(1 / calculated_duration * beat_type)
                # print(f"Calculated bigger note duration {calculated_duration}")

            else:
                calculated_duration = beat_type

            # Convert pitch information to standard notation
            if is_rest:
                notes_list.append("REST")
                durations_list.append(int(calculated_duration))
                continue
            pitch = note_elem.find(".//pitch")
            note = pitch.find("step").text
            # print(f"Note {note}")
            # input("Press enter to continue...")
            alter = (
                int(pitch.find("alter").text) if pitch.find("alter") is not None else 0
            )
            octave = int(pitch.find("octave").text)

            # Represent dotted notes with negative durations
            if is_dotted:
                calculated_duration *= -1
            notes_list.append(f"{note}{'S' * alter}{octave}")
            durations_list.append(calculated_duration)

    return notes_list, durations_list, tempo
