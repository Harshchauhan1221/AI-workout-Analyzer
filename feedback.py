import pyttsx3

engine = pyttsx3.init()

# 🔊 General speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()


# 🎯 Posture feedback logic
def posture_feedback(angle):
    if angle is None:
        return ""

    if angle < 60:
        feedback = "Too low"
    elif 60 <= angle <= 120:
        feedback = "Good form"
    else:
        feedback = "Too high"

    return feedback