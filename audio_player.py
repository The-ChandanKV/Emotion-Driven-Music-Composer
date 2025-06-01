import pygame
import threading
import time
import os

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.is_playing = False
        self.play_thread = None
    
    def play(self, midi_file_path):
        # Stop any currently playing music
        self.stop()
        
        try:
            # Start playing new music
            pygame.mixer.music.load(midi_file_path)
            pygame.mixer.music.play()
            self.current_music = midi_file_path
            self.is_playing = True
            
            # Start a thread to monitor the playback
            self.play_thread = threading.Thread(target=self._monitor_playback)
            self.play_thread.daemon = True
            self.play_thread.start()
            
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.current_music = None
            
            # Wait for monitoring thread to finish
            if self.play_thread and self.play_thread.is_alive():
                self.play_thread.join()
    
    def _monitor_playback(self):
        while self.is_playing and pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        # Clean up when music ends
        self.is_playing = False
        self.current_music = None 