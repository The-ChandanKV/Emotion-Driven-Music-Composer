import random
import os
from midiutil import MIDIFile

class MusicComposer:
    def __init__(self):
        self.emotion_mappings = {
            'happy': {
                'scale': [60, 62, 64, 65, 67, 69, 71, 72],  # C major scale
                'tempo': 120,
                'velocity': 100,
                'note_lengths': [1, 0.5, 0.25]  # whole, half, quarter notes
            },
            'sad': {
                'scale': [57, 59, 60, 62, 64, 65, 67, 69],  # A minor scale
                'tempo': 75,
                'velocity': 70,
                'note_lengths': [2, 1, 0.5]
            },
            'angry': {
                'scale': [64, 66, 67, 69, 71, 72, 74, 76],  # E minor scale
                'tempo': 140,
                'velocity': 120,
                'note_lengths': [0.25, 0.5, 0.25]
            },
            'neutral': {
                'scale': [67, 69, 71, 72, 74, 76, 78, 79],  # G major scale
                'tempo': 95,
                'velocity': 85,
                'note_lengths': [1, 0.5, 0.25]
            }
        }
        self.default_emotion = 'neutral'
    
    def _create_melody(self, emotion_params, num_measures=4):
        # Create MIDI file with 1 track
        midi = MIDIFile(1)
        track = 0
        time = 0
        
        # Setup the track
        midi.addTempo(track, time, emotion_params['tempo'])
        
        # Create measures
        for _ in range(num_measures):
            # 4 beats per measure
            beats_remaining = 4
            
            while beats_remaining > 0:
                # Choose note length
                note_length = random.choice(emotion_params['note_lengths'])
                if note_length > beats_remaining:
                    note_length = beats_remaining
                
                # Choose pitch from scale
                pitch = random.choice(emotion_params['scale'])
                
                # Add note to track
                midi.addNote(track, 0, pitch, time, note_length, 
                           emotion_params['velocity'])
                
                time += note_length
                beats_remaining -= note_length
        
        return midi
    
    def compose(self, emotion):
        # Get emotion parameters
        emotion = emotion.lower()
        if emotion not in self.emotion_mappings:
            emotion = self.default_emotion
        
        emotion_params = self.emotion_mappings[emotion]
        
        # Generate melody
        midi = self._create_melody(emotion_params)
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Save as MIDI file
        output_path = os.path.join('output', f'emotion_{emotion}.mid')
        with open(output_path, 'wb') as f:
            midi.writeFile(f)
        
        return output_path 