def analyze_emotion(text):
    text = text.lower()
    if any(word in text for word in ["stressed", "anxious", "overwhelmed", "panic", "can't focus"]):
        return "anxious"
    elif any(word in text for word in ["sad", "depressed", "low", "lonely", "tired"]):
        return "depressed"
    elif any(word in text for word in ["angry", "mad", "frustrated", "pissed"]):
        return "angry"
    elif any(word in text for word in ["happy", "excited", "grateful", "glad", "joy"]):
        return "happy"
    elif any(word in text for word in ["motivated", "inspired", "focused", "ready"]):
        return "motivated"
    else:
        return None
