accuracy_history = []

def calculate_accuracy(angle, exercise):

    # 🎯 Exercise-specific ideal angles
    if exercise == "Squat":
        ideal = 100
    elif exercise == "Pushup":
        ideal = 90
    elif exercise == "Bicep Curl":
        ideal = 45
    elif exercise == "Shoulder Press":
        ideal = 90
    elif exercise == "Front Double Biceps":
        ideal = 80
    elif exercise == "Side Chest":
        ideal = 70
    else:
        ideal = 100

    # 📊 Raw accuracy
    accuracy = max(0, 100 - abs(angle - ideal))

    # 🔥 Remove noise
    if accuracy < 20:
        return None

    accuracy_history.append(accuracy)
    return accuracy