# MusicXML to Arduino Melody Converter

This project provides a script that converts MusicXML files into melodies that can be played by a [well-known Arduino sketch](https://github.com/robsoncouto/arduino-songs). It allows you to easily generate Arduino code for playing melodies from sheet music.

## Features :musical_note:

- Converts MusicXML files into Arduino-compatible melody code
- Can generate .ino scripts ready for upload
- Provides options for customizing the generated Arduino code, such as tempo and pin configuration
- Easy to integrate into your Arduino projects

## Getting Started

To get started with the MusicXML to Arduino Melody Converter, follow these steps:

1. Clone the repository: `git clone https://github.com/Luisao-official/Arduino-music.git` (or download  and extract the zip file)
1. Run the script: `python ardu_music.py`
2. The converted Arduino code will be generated in the output directory.

## Usage

The script accepts a MusicXML file as input and generates Arduino code that plays the melody on an Arduino board. You can change variables such as tempo and pin configuration to customize the generated code.

The .musicxml files have to be inside a folder, and you'll provide the path to its root, like "D:/root/example_music/example.musicxml" (for Windows). This is because you can have more than one .musicxml file for a song, and the script will convert them all at once.

You can convert midi files to MusicXML using [MuseScore](https://musescore.org/en) or the [Romot Online converted](https://romot-co.github.io/midi-musicxml-seq/).

If you want to edit the melody, you can edit the midi format on your favorite DAW, or [Signal](https://signal.vercel.app/edit) online editor and then convert it to MusicXML.

For detailed usage instructions, please take a look at the [documentation](docs/usage.md).

## Examples

To help you get started, we have provided some example MusicXML files in the [examples](examples/EXAMPLES.md) directory. You can use these files to test the converter and see how the generated Arduino code sounds.


## Issues and TODOs

- Consider using .midi files for better efficiency and compatibility.
- Improve MusicXML parsing and add more automation features, such as automated key signature detection and separation of harmonies.




## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request. For more information, see our [contribution guidelines](CONTRIBUTING.md).

##Credits

The Arduino script is based on [Robson Couto's](https://github.com/robsoncouto) work

## License

This project is licensed under the [MIT License](LICENSE).
