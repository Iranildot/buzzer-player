from serial_connection import *
from sheet_music_manager import *
from timer import *
from customtkinter import *
from tkinter.filedialog import askopenfile
from PIL import Image

class App(CTk):
    def __init__(self) -> None:
        super().__init__()
        
        # DEFINING ARDUINO'S VARIABLES
        self.serial_connection = SerialConnection()
        self.ports = self.serial_connection.check_available_ports()["ports"]
        self.arduino = None
        
        # DEFINING SONG'S VARIABLES
        self.manager = SheetMusicManager()
        self.path = None
        self.song = None
        self.song_started = False
        self.parts_index = None
        self.parts_started = None
        self.song_duration = 0
        self.minutes_duration = 0
        self.seconds_duration = 0
        self.song_timer = 0
        self.song_not_paused = True
        
        # SETTING WINDOW CONFIGURATION
        self.title("Buzzer player") # TITLE
        self.geometry("700x200+200+200") # GEOMETRY
        self._set_appearance_mode("dark") # THEME MODE
        set_widget_scaling(1.2) 
        self.protocol("WM_DELETE_WINDOW", self.cancel) # WHEN THE WINDOW IS CLOSED
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # CREATING THE MAIN FRAME
        self.main_frame = CTkFrame(self, bg_color="#242424", fg_color="#242424")
        self.main_frame.grid()
        
        # CREATING THE LEFT FRAME TO USER SET UP ARDUINO CONNECTION
        self.left_frame = CTkFrame(self.main_frame, bg_color="#242424", fg_color="#242424")
        self.left_frame.rowconfigure(0, weight=1)
        self.left_frame.grid(sticky="NS")
        
        # LEFT LABEL
        self.connected_arduino_label = CTkLabel(self.left_frame,
                                                text="CONNECTED DEVICE",
                                                bg_color="#242424",
                                                fg_color="#242424",
                                                text_color="#FFFFFF",
                                                compound="left",
                                                image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
        self.connected_arduino_label.grid(pady=10, sticky="w")
        
        # LEFT COMBOBOX TO ARDUINO CONNECTION
        self.connected_arduino_combobox = CTkComboBox(self.left_frame,
                                                      bg_color="#242424",
                                                      width=180,
                                                      values=self.ports,
                                                      command=self.connect_arduino)
        self.connected_arduino_combobox.grid(row=1, column=0, padx=(0, 20))
        
        # RIGHT FRAME TO STORE SONGS THINGS
        self.right_frame = CTkFrame(self.main_frame,
                                    bg_color="#242424",
                                    fg_color="#242424")
        self.right_frame.grid(row=0, column=1)
        
        # BUTTON TO BROWSE SONGS
        self.browse_button = CTkButton(self.right_frame,
                                       bg_color="#242424",
                                       fg_color="#242424",
                                       border_width=2,
                                       text="Browse",
                                       command=self.shearch_file)
        self.browse_button.grid(row=0, column=0, pady=10, columnspan=2, sticky="EW")
        
        # BUTTON TO PLAY/PAUSE SONGS
        self.play_pause_button = CTkButton(self.right_frame,
                                      text="Play",
                                      bg_color="#242424",
                                      fg_color="#242424", 
                                      border_width=2,
                                      image=CTkImage(light_image=Image.open("./icons/play_pause.png")),
                                      command=self.play_song)
        self.play_pause_button.grid(row=1, column=0, padx=(0, 10))
        
        # LABEL THAT SHOWS THE USER THE TIME EACH SONG HAS AND HOW MUCH TIME THE CURRENT PLAYING SONG HAS TO FINISH 
        self.song_time_frame = CTkLabel(self.right_frame,
                                        text="00:00/00:00",
                                        bg_color="#242424",
                                        fg_color="#242424",
                                        text_color="#FFFFFF",
                                        compound="left")
        self.song_time_frame.grid(row=1, column=1, padx=10)
        
        # CHECKING IF THERE ARE ARDUINOS CONNECTED TO COMPUTER USB PORTS
        self.checking_divices()
        
        # IF THERE ARE/IS ANY DEVICE PLUGGED IN TRY TO CONNECT TO THE COMPUTER VIA SERIAL CONNECTION
        if self.connected_arduino_combobox.get() != "":
            try:
                self.arduino = self.serial_connection.start(self.connected_arduino_combobox.get())
                self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb.png")))
            except:
                self.connected_arduino_combobox.set(value=[])
                self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
                self.alert_window("ARDUINO CONNECTION FAILED")
                
    # TO STABILISH SERIAL CONNECTION
    def connect_arduino(self, event) -> None:
        if self.arduino != None:
            self.serial_connection.end(self.arduino)
        
        try:
            self.arduino = self.serial_connection.start(self.connected_arduino_combobox.get())
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb.png")))
            self.song_started = False
            self.song_not_paused = True
            self.play_pause_button.configure(text="Play")
        except:
            self.connected_arduino_combobox.set(value=[])
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
            self.alert_window("ARDUINO CONNECTION FAILED")
    
    # TO SEARCH SONG FILES
    def shearch_file(self) -> None:
        self.path = askopenfile(title="Browse file") # ASK FOR A FILE
        
        if self.path != None:
            if ".mid" == self.path.name[-4:]:
                self.browse_button.configure(text="..." + self.path.name[-20:])
                self.song_started = False
                self.song_not_paused = True
                self.play_pause_button.configure(text="Play")
            
                self.song = self.manager.extract_notes_info(self.path.name)       
                self.reestart_song()      
            
                self.minutes_duration = int(self.song_duration // 60)
                self.seconds_duration = int(self.song_duration % 60)
                self.song_time_frame.configure(text=f"00:00/{self.minutes_duration:02}:{self.seconds_duration:02}")
            else:
                self.alert_window("THAT'S NOT A MIDI FILE")
    
    def reestart_song(self) -> None:
        try:
            self.parts_index = [0 for i in range(len(self.song)) if i < 4]
            self.parts_started = [False for i in range(len(self.song)) if i < 4]

            aux = []
            
            self.song_duration = 0
            
            # TO DETERMINE THE DURATION OF THE SONG
            for part in range(4):
                if len(self.song) - 1 >= part:
                    aux.append(self.song[part])
                    for frequency, duration in self.song[part]:
                        self.song_duration += duration
            self.song = aux
        except:
            pass
            
    # TO CHECK IF THERE ARE ARDUINOS CONNECTED TO THE USB PORTS ON USER'S COMPUTER
    def checking_divices(self) -> None:               
        
        # GETTING THE PORT
        self.ports = self.serial_connection.check_available_ports()["ports"]
        # PUT THE PORTS INTO COMBOBOX VALUES
        self.connected_arduino_combobox.configure(values=self.ports)
        
        if self.connected_arduino_combobox.get() not in self.ports:
            self.song_started = False
            self.song_not_paused = True
            self.connected_arduino_combobox.set(value="")
            self.connected_arduino_label.configure(image=CTkImage(light_image=Image.open("./icons/usb_off.png")))
        
        # CHECKS THE USB PORTS EACH 2 SECONDS
        self.after(2000, self.checking_divices)
    
    def reestart_song_settings(self):
        self.song_started = True
        self.song_not_paused = True
        self.song_timer = 0
        self.play_pause_button.configure(text="Play")
        self.reestart_song()
        self.alert_window("DEVICE NOT CONNECTED")
    
    def play_song(self) -> None:
        if self.song != None:
            self.song_not_paused = not self.song_not_paused
            
            # TO START PLAYING THE SONG
            if self.song_not_paused == False and self.song_started == False:
                self.song_started = True
                self.song_timer = 0
                self.reestart_song()
                self.play_pause_button.configure(text="Pause")
            
            # TO PAUSE/UNPAUSE THE SONG
            else:
                self.play_pause_button.configure(text="Play" if self.play_pause_button._text == "Pause" else "Pause")
            
            while True:
                
                self.update()
                # TO CHECK IF THE USER INTERRUPT THE SONG
                if not self.song_started:
                    return
                
                if self.song_not_paused == False:
                    for index in range(len(self.song)):
                        self.update()
                        
                        # TO CHECK IF THE USER INTERRUPT THE SONG
                        if not self.song_started:
                            return
                            
                        while True:
                            # TO CHECK IF THE USER INTERRUPT THE SONG
                            if not self.song_started:
                                return
                            
                            # TO KNOW WHEN THE NOTE'S DURATION ENDS
                            try:
                                if self.arduino.inWaiting():
                                    # GET THE ARUINO RESPONSE
                                    response = int(self.arduino.read().decode())
                                    # UPDATE THE SONG DURATION
                                    self.song_timer += self.song[response][self.parts_index[response]][1]
                                    self.parts_started[response] = False
                                    # UPDATE THE DURATION ON SCREEN
                                    self.song_time_frame.configure(text=f"{int(self.song_timer // 60):02}:{int(self.song_timer % 60):02}/{self.minutes_duration:02}:{self.seconds_duration:02}")                            
                                else:
                                    break
                            except:
                                self.reestart_song_settings()
                                return
                            
                        
                        if self.parts_index[index] < len(self.song[index]) - 1:
                            if self.parts_started[index] == False:
                                
                                # TO CHECK IF THE USER INTERRUPT THE SONG
                                if not self.song_started:
                                    return
                                
                                # SET UP THE DATA TO SEND IT TO ARDUINO
                                self.parts_index[index] += 1
                                frequency, duration = self.song[index][self.parts_index[index]]
                                
                                # TO SEND INDEX, FREQUENCY AND DURATION OF SONG'S NOTES
                                try:
                                    self.arduino.write(f"{index}:{frequency}:{round(duration*1000)}\r\n".encode())
                                except:
                                    self.reestart_song_settings()
                                    return
                                
                                # TO WAIT UNTIL THE COMPUTER RECIVE THE ARDUINO RESPONSE
                                while True:
                                    
                                    # TO CHECK IF THE USER INTERRUPT THE SONG
                                    if not self.song_started:
                                        return
                                    
                                    try:
                                        if self.arduino.inWaiting():
                                            response = int(self.arduino.read().decode())
                                            
                                            # WHEN THE NOTE'S DURATION ENDS
                                            if response != 5:
                                                self.song_timer += self.song[response][self.parts_index[response]][1]
                                                self.parts_started[response] = False
                                                self.song_time_frame.configure(text=f"{int(self.song_timer // 60):02}:{int(self.song_timer % 60):02}/{self.minutes_duration:02}:{self.seconds_duration:02}")
                                            
                                            # CHECKING IF THE ARDUINO RECIVES THE DATA AND ANSWERS BACK
                                            else:
                                                time.sleep(0.01)
                                                break
                                    
                                    # IF OCCURS AN ERROR
                                    except:
                                        self.reestart_song_settings()
                                        return
                                    
                                self.parts_started[index] = True
                    
                    # WHEN THE SONG FINISH
                    if len(self.song) == len([True for i in range(len(self.parts_index)) if self.parts_index[i] >= len(self.song[i]) - 1]) or not self.song_started:
                        self.song_time_frame.configure(text=f"{self.minutes_duration:02}:{self.seconds_duration:02}/{self.minutes_duration:02}:{self.seconds_duration:02}")
                        break
            
            # TO REESTART THE PLAYER PARAMS
            self.play_pause_button.configure(text="Play")
            self.song_started = False
            self.song_not_paused = True
        else:
            self.alert_window("NO MIDI FILE WAS SELECTED")
        
    # TO STOP THE SONG LOOP WHEN THE APP WINDOW CLOSE
    def cancel(self) -> None:
        self.song_started = False
        
        if self.arduino != None:
            self.serial_connection.end(self.arduino)
            
        self.quit()
    
    def alert_window(self, message:str) -> None:
        self.window = CTkToplevel(self)
        self.window.attributes('-topmost', True)
        self.window.geometry("+200+200")
        self.window.resizable(False, False)
        self.window.columnconfigure(0, weight=1)
        
        self.window_frame = CTkFrame(self.window, bg_color="#242424", fg_color="#242424")
        self.window_frame.grid()
        CTkLabel(self.window_frame, text=message, text_color="#FFFFFF").grid(padx=30, pady=(20, 5))
        CTkButton(self.window_frame, text="OK", command=lambda: self.window.destroy()).grid(padx=(0, 30), pady=(5, 20), sticky="E")

if __name__ == "__main__":
    app = App()
    app.mainloop()