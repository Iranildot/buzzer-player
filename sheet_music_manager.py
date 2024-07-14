import music21 as m21

class SheetMusicManager:
    def __init__(self) -> None:
        self.notes_info = []
        
    def note_to_frequency(self, note_name):
        pitch = m21.pitch.Pitch(note_name)
        return round(pitch.frequency)
    
    def extract_notes_info(self, file_path) -> list:
        
        if ".mid" in file_path:
            
            score = m21.converter.parse(file_path) # OPEN MIDI FILE
            self.notes_info = [[] for _ in range(len(score.parts))] # TO KEEP SOME NOTES INFORMATION

            for part_index, part in enumerate(score.parts):
                for element in part.flatten().notesAndRests:  # Inclui pausas na iteração
                    if isinstance(element, m21.note.Note):
                        note_name = element.nameWithOctave
                        frequency = self.note_to_frequency(note_name)
                        duration = element.quarterLength
                        self.notes_info[part_index].append((frequency, duration*0.5))
                    elif isinstance(element, m21.note.Rest):
                        duration = element.quarterLength
                        self.notes_info[part_index].append(("REST", duration*0.5))
            
            return self.notes_info
        
        else:
            
            return None