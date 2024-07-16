# Buzzer Player
## Overview

Buzzer Player is a Python-based GUI application designed to interface with an Arduino to play MIDI files through a buzzer. Utilizing the customtkinter library for an enhanced visual appearance, the application allows users to select and play MIDI files, displaying the current playtime and total duration.

## Features

- **Arduino Integration**: Automatically detects connected Arduino devices and establishes a serial connection.
- **MIDI File Support**: Users can browse and select MIDI files to be played through the buzzer connected to the Arduino.
- **Real-Time Playback Display**: Shows the elapsed and total duration of the current song.
- **Play/Pause Functionality**: Easily control the playback of MIDI files with a single button.
- **Custom Theme**: Utilizes a dark theme for a modern and visually appealing user interface.

## Libraries Used

- **serial_connection**: Manages the serial connection to the Arduino.
- **sheet_music_manager**: Handles the processing and management of MIDI files.
- **timer**: Manages timing functions for playback.
- **customtkinter**: Provides custom-styled widgets for the GUI.
- **tkinter**: Standard Python interface to the Tk GUI toolkit.
- **PIL**: Python Imaging Library for image processing.

## Installation

- **Clone the Repository**:

```bash```
```git clone https://github.com/your-username/buzzer-player.git cd buzzer-player```

- **Install Dependencies**:

```bash```
```pip install -r requirements.txt```

## Usage

- **Connect Arduino**: Ensure your Arduino is connected to your computer's USB port and the .ino program is installed in your device.
- **Run the Application**:

```bash``` 
```python app.py```

- **Select MIDI File**: Use the "Browse" button to select a MIDI file from your computer.
- **Play/Pause**: Control playback with the "Play" button, which toggles between play and pause states.
- **Monitor Playback**: The application displays the current and total playtime of the MIDI file.

## Code Structure

- **App Class**: The main application class that initializes and manages the GUI, Arduino connection, and song playback.
- **connect_arduino**: Establishes a serial connection to the selected Arduino device.
- **shearch_file**: Opens a file dialog for selecting MIDI files.
- **play_song**: Manages the playback loop, sending commands to the Arduino and updating the GUI.
- **alert_window**: Displays alert messages in a separate window.

## How the app looks like

![buzzer player defult page](https://github.com/user-attachments/assets/7d48d762-77fa-4631-84a7-1138572a2223)

## How the circuit looks like

![buzzer player circuit](https://github.com/user-attachments/assets/5407f215-68c4-416f-9b25-1c300849ff96)

## Contributing

Feel free to open issues or submit pull requests if you have any suggestions or improvements.

## License

This project is licensed under the MIT License.

