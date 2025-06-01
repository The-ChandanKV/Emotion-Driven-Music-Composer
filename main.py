import sys
import tkinter as tk
from tkinter import ttk
import cv2
import threading
from emotion_detector.face_detector import FaceEmotionDetector
from emotion_detector.voice_detector import VoiceEmotionDetector
from music_generator.composer import MusicComposer
from utils.audio_player import AudioPlayer

class EmotionMusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion-Driven Music Composer")
        self.root.geometry("800x600")
        
        # Initialize components
        self.face_detector = FaceEmotionDetector()
        self.voice_detector = VoiceEmotionDetector()
        self.composer = MusicComposer()
        self.audio_player = AudioPlayer()
        
        self.setup_ui()
        self.is_running = False
        self.current_mode = None
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Mode selection
        ttk.Label(main_frame, text="Select Input Mode:", font=('Helvetica', 14)).grid(row=0, column=0, pady=10)
        
        # Buttons
        ttk.Button(main_frame, text="Webcam Mode", command=self.start_webcam_mode).grid(row=1, column=0, pady=5)
        ttk.Button(main_frame, text="Voice Mode", command=self.start_voice_mode).grid(row=2, column=0, pady=5)
        ttk.Button(main_frame, text="Stop", command=self.stop_detection).grid(row=3, column=0, pady=5)
        
        # Status display
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var, font=('Helvetica', 12)).grid(row=4, column=0, pady=20)
        
        # Emotion display
        self.emotion_var = tk.StringVar(value="No emotion detected")
        ttk.Label(main_frame, textvariable=self.emotion_var, font=('Helvetica', 16)).grid(row=5, column=0, pady=10)
    
    def start_webcam_mode(self):
        if not self.is_running:
            self.is_running = True
            self.current_mode = "webcam"
            self.status_var.set("Starting webcam...")
            threading.Thread(target=self.webcam_detection_loop, daemon=True).start()
    
    def start_voice_mode(self):
        if not self.is_running:
            self.is_running = True
            self.current_mode = "voice"
            self.status_var.set("Starting voice detection...")
            threading.Thread(target=self.voice_detection_loop, daemon=True).start()
    
    def stop_detection(self):
        self.is_running = False
        self.status_var.set("Stopped")
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
    
    def webcam_detection_loop(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_var.set("Error: Could not open webcam")
            return
        
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                emotion = self.face_detector.detect_emotion(frame)
                self.update_emotion_display(emotion)
                self.generate_music(emotion)
            
            self.root.update()
        
        self.cap.release()
    
    def voice_detection_loop(self):
        while self.is_running:
            emotion = self.voice_detector.detect_emotion()
            self.update_emotion_display(emotion)
            self.generate_music(emotion)
    
    def update_emotion_display(self, emotion):
        self.emotion_var.set(f"Detected Emotion: {emotion}")
    
    def generate_music(self, emotion):
        music = self.composer.compose(emotion)
        self.audio_player.play(music)

def main():
    root = tk.Tk()
    app = EmotionMusicApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 