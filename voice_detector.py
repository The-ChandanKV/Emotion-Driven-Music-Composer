import numpy as np
import sounddevice as sd
import threading
import queue
from scipy import signal

class VoiceEmotionDetector:
    def __init__(self):
        self.emotions = ['neutral', 'happy', 'sad', 'angry']
        self.sample_rate = 16000
        self.duration = 3  # Record 3 seconds of audio at a time
        self.audio_queue = queue.Queue()
    
    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Error in audio callback: {status}")
            return
        self.audio_queue.put(indata.copy())
    
    def analyze_audio(self, audio_data):
        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Calculate audio features
        # 1. Volume (RMS energy)
        rms = np.sqrt(np.mean(np.square(audio_data)))
        
        # 2. Zero crossing rate
        zero_crossings = np.sum(np.abs(np.diff(np.signbit(audio_data))))
        zcr = zero_crossings / len(audio_data)
        
        # 3. Spectral centroid
        frequencies, power_spectrum = signal.welch(audio_data, self.sample_rate)
        spectral_centroid = np.sum(frequencies * power_spectrum) / np.sum(power_spectrum)
        
        # Simple rule-based emotion classification
        if rms > 0.1:  # High volume
            if zcr > 0.1:  # High zero-crossing rate
                return 'angry'
            else:
                return 'happy'
        else:  # Low volume
            if spectral_centroid > 2000:  # High frequency content
                return 'neutral'
            else:
                return 'sad'
    
    def detect_emotion(self):
        try:
            with sd.InputStream(channels=1,
                              samplerate=self.sample_rate,
                              callback=self.audio_callback,
                              blocksize=int(self.sample_rate * self.duration)):
                
                # Get audio data from queue
                audio_data = self.audio_queue.get(timeout=self.duration + 1)
                
                # Analyze audio and determine emotion
                emotion = self.analyze_audio(audio_data)
                return emotion
                
        except Exception as e:
            print(f"Error in voice detection: {e}")
            return "neutral" 