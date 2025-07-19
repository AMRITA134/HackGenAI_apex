from deepface import DeepFace
import cv2
import time
import json
import threading
import websocket  # pip install websocket-client

USE_MOCK_MODE = False     # Toggle this to True to test without webcam
PLAYER_NAME = "P1"        # Change for P2 if needed
WS_URL = "ws://localhost:8080"  # Change to your Godot WebSocket server

cooldown = 3  # Seconds between sends
last_sent_time = 0

# Predefined emotions for mock mode
mock_emotions = ["happy", "sad", "angry", "neutral", "surprise"]

# Setup websocket connection
try:
    ws = websocket.create_connection(WS_URL)
    print("[Connected] WebSocket to Godot at", WS_URL)
except Exception as e:
    print("WebSocket Error:", e)
    exit()

# Send emotion data as JSON
def send_emotion(emotion):
    global last_sent_time
    if time.time() - last_sent_time < cooldown:
        return
    last_sent_time = time.time()

    data = {
        "player": PLAYER_NAME,
        "emotion": emotion
    }
    try:
        ws.send(json.dumps(data))
        print(f"[Sent] {data}")
    except Exception as e:
        print("[Send Error]", e)

# Real mode: detect via DeepFace
def real_mode():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            cv2.putText(frame, f'Emotion: {emotion}', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            send_emotion(emotion)
        except:
            pass

        cv2.imshow('Emotion Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Mock mode: manually simulate emotions
def mock_mode():
    print("[Mock Mode] Press keys: H=Happy, A=Angry, S=Sad, N=Neutral, Q=Quit")
    while True:
        key = input("Enter emotion (h/a/s/n/q): ").lower()
        if key == 'q':
            break
        key_map = {
            'h': 'happy',
            'a': 'angry',
            's': 'sad',
            'n': 'neutral'
        }
        if key in key_map:
            send_emotion(key_map[key])
        else:
            print("Invalid key. Try h/a/s/n.")

# Entry point
if __name__ == "__main__":
    try:
        if USE_MOCK_MODE:
            mock_mode()
        else:
            real_mode()
    except KeyboardInterrupt:
        print("Exiting...")
    ws.close()
