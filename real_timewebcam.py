import cv2
import time
import json
import socket
import threading
from deepface import DeepFace

# === CONFIGURATION ===
USE_MOCK_MODE = False
PLAYER_NAME = "P1"
TCP_IP = "127.0.0.1"
TCP_PORT = 9090

cooldown = 30  # seconds between emotion detection and send
last_sent_time = 0

# === SETUP TCP SOCKET CLIENT ===
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((TCP_IP, TCP_PORT))
    print(f"[Connected] TCP to Godot at {TCP_IP}:{TCP_PORT}")
except Exception as e:
    print("TCP connection error:", e)
    exit()

# === FUNCTION TO SEND EMOTION DATA ===
def send_emotion(emotion):
    global last_sent_time
    if time.time() - last_sent_time < cooldown:
        return
    last_sent_time = time.time()

    data = {
        "player": PLAYER_NAME,
        "emotion": emotion
    }

    def send_thread():
        try:
            msg = json.dumps(data) + "\n"
            sock.sendall(msg.encode('utf-8'))
            print(f"[Sent] {data}")
        except Exception as e:
            print("[Send Error]", e)

    threading.Thread(target=send_thread, daemon=True).start()

# === REAL-TIME EMOTION DETECTION ===
def real_mode():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return

    last_detect_time = 0
    detect_interval = 30  # seconds

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            now = time.time()
            if now - last_detect_time >= detect_interval:
                try:
                    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='opencv')
                    emotion = result[0]['dominant_emotion']
                    print(f"[Detected] Emotion: {emotion}")
                    send_emotion(emotion)
                    last_detect_time = now
                except Exception as e:
                    print("Emotion detection error:", e)

            cv2.putText(frame, 'Detecting every 30s', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Emotion Detection (30s)', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        sock.close()

# === MAIN ===
if __name__ == "__main__":
    try:
        if USE_MOCK_MODE:
            print("Mock mode not used in this version.")
        else:
            real_mode()
    except KeyboardInterrupt:
        print("Exiting...")
        sock.close()
