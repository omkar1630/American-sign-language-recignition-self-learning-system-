# American Sign Language Recognition – Self-Learning System

A rule-based American Sign Language (ASL) recognition system that detects hand gestures using predefined logical conditions. It analyzes hand shape, finger positions, and orientation, then matches them to stored rules for accurate gesture identification. The system is fast, interpretable, and useful for basic ASL communication.

---

## Features
- Rule-based gesture detection (no machine learning required)
- Real-time hand tracking
- Self-learning capability to improve gesture recognition
- Detects basic ASL hand signs
- Easy to extend with custom rules

---

## How It Works
1. The system captures a hand gesture via webcam or image input.
2. Features such as finger positions, hand orientation, and palm openness are extracted.
3. These features are compared against predefined rules stored in the system.
4. The gesture is recognized and translated into corresponding text.

---

## Project Structure
/American-sign-language-recognition-self-learning-system
│-- db/ # Database or data storage files
│-- handTracking/ # Hand tracking and gesture detection scripts
│-- static/ # Static assets (images, CSS, JS)
│-- templates/ # HTML templates (if using web interface)
│-- app.py # Main application script
│-- site.db # Database file
│-- README.md # Project documentation


---

## Technologies Used
- Python  
- OpenCV (for hand tracking)  
- Rule-based logic (if-else conditions for gesture recognition)  
- SQLite (for storing gesture data)

---

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/omkar1630/American-sign-language-recognition-self-learning-system.git

 ## install dependencies (if required):

pip install opencv-python


## Run the main script:

python app.py
