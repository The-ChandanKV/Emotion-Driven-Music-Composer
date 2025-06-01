import cv2
import numpy as np

class FaceEmotionDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotions = ['neutral', 'happy', 'sad', 'angry']
        
    def detect_emotion(self, frame):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Get the largest face
            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            
            # Extract face ROI
            face_roi = gray[y:y+h, x:x+w]
            
            # Simple emotion detection based on image statistics
            mean_intensity = np.mean(face_roi)
            std_intensity = np.std(face_roi)
            
            # Simple rule-based emotion classification
            if std_intensity > 65:  # High variation might indicate expression
                if mean_intensity > 130:
                    emotion = 'happy'
                else:
                    emotion = 'angry'
            else:  # Low variation might indicate neutral or sad
                if mean_intensity > 110:
                    emotion = 'neutral'
                else:
                    emotion = 'sad'
            
            # Draw rectangle and emotion label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, emotion, (x, y-10),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            return emotion
        
        return 'neutral' 