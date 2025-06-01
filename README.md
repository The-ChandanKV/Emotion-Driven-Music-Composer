# Emotion-Driven Music Composer

An AI-powered application that generates music based on detected emotions through facial expressions or voice input.

## Features
- Real-time emotion detection through webcam
- Voice-based emotion detection
- Custom music generation based on detected emotions
- Support for multiple musical styles
- Real-time music composition and playback

## Tech Stack
- Python 3.8+
- TensorFlow for deep learning
- OpenCV for image processing
- Music21 for music composition
- MediaPipe for face detection
- Librosa for audio processing

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Launch the application
2. Choose input mode (webcam or voice)
3. Allow access to your camera/microphone
4. The application will detect your emotions and generate music in real-time

## Project Structure
- `main.py`: Main application entry point
- `emotion_detector/`: Emotion detection modules
  - `face_detector.py`: Facial emotion detection
  - `voice_detector.py`: Voice emotion detection
- `music_generator/`: Music generation modules
  - `composer.py`: Music composition logic
  - `models.py`: Neural network models
- `utils/`: Utility functions
- `models/`: Pre-trained model weights

## Note
Make sure you have a working webcam and/or microphone for the best experience. 
