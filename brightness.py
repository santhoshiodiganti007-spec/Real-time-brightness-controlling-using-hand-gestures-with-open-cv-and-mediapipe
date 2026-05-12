import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
from math import hypot
import screen_brightness_control as sbc
import numpy as np
import urllib.request, os
from datetime import datetime

# Download model if not present
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmark model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task",
        MODEL_PATH
    )
    print("Download complete!")

# Setup HandLandmarker
base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.75,
    min_hand_presence_confidence=0.75,
    min_tracking_confidence=0.75
)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

# Button state
captured_msg = ""
captured_timer = 0

# Button definitions [label, x, y, w, h, color]
BTN_CAPTURE = {"label": "Capture", "x": 10,  "y": 60, "w": 120, "h": 45, "color": (34, 139, 34)}
BTN_STOP    = {"label": "Stop",    "x": 140, "y": 60, "w": 120, "h": 45, "color": (0, 0, 200)}

def draw_button(frame, btn, hover=False):
    color = tuple(min(c + 40, 255) for c in btn["color"]) if hover else btn["color"]
    x, y, w, h = btn["x"], btn["y"], btn["w"], btn["h"]
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
    text_size = cv2.getTextSize(btn["label"], cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
    tx = x + (w - text_size[0]) // 2
    ty = y + (h + text_size[1]) // 2
    cv2.putText(frame, btn["label"], (tx, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def is_hover(btn, mx, my):
    return btn["x"] < mx < btn["x"] + btn["w"] and btn["y"] < my < btn["y"] + btn["h"]

mouse_x, mouse_y = 0, 0
click_flag = False

def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y, click_flag
    mouse_x, mouse_y = x, y
    if event == cv2.EVENT_LBUTTONDOWN:
        click_flag = True

cv2.namedWindow('Brightness Control')
cv2.setMouseCallback('Brightness Control', mouse_callback)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Convert to MediaPipe Image
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    # Detect hands
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            for lm in hand_landmarks:
                cx, cy = int(lm.x * width), int(lm.y * height)
                cv2.circle(frame, (cx, cy), 4, (0, 255, 0), cv2.FILLED)

            x_1 = int(hand_landmarks[4].x * width)
            y_1 = int(hand_landmarks[4].y * height)
            x_2 = int(hand_landmarks[8].x * width)
            y_2 = int(hand_landmarks[8].y * height)

            cv2.circle(frame, (x_1, y_1), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x_2, y_2), 7, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)

            L = hypot(x_2 - x_1, y_2 - y_1)
            b_level = np.interp(L, [15, 220], [0, 100])
            sbc.set_brightness(int(b_level))

            cv2.putText(frame, f'Brightness: {int(b_level)}%',
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)

    # Draw buttons with hover effect
    draw_button(frame, BTN_CAPTURE, hover=is_hover(BTN_CAPTURE, mouse_x, mouse_y))
    draw_button(frame, BTN_STOP,    hover=is_hover(BTN_STOP,    mouse_x, mouse_y))

    # Handle clicks
    if click_flag:
        if is_hover(BTN_CAPTURE, mouse_x, mouse_y):
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(filename, frame)
            captured_msg = f"Saved: {filename}"
            captured_timer = 60  # show message for ~2 seconds
            print(f"Screenshot saved: {filename}")

        elif is_hover(BTN_STOP, mouse_x, mouse_y):
            break

        click_flag = False

    # Show capture confirmation message
    if captured_timer > 0:
        cv2.putText(frame, captured_msg, (10, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        captured_timer -= 1

    cv2.imshow('Brightness Control', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()