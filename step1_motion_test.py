import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

cap = cv2.VideoCapture(0)

prev_y = None
last_tap_time = 0

PIXEL_TAP_THRESHOLD = 20   # adjust if needed (20–30)
COOLDOWN = 0.5             # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    text = "deltaY: ---"

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark[8]  # index finger tip

        cx = int(lm.x * w)
        cy = int(lm.y * h)

        cv2.circle(frame, (cx, cy), 12, (0, 255, 0), -1)

        if prev_y is not None:
            delta = cy - prev_y
            text = f"deltaY: {delta}"

            now = time.time()
            if delta > PIXEL_TAP_THRESHOLD and (now - last_tap_time) > COOLDOWN:
                last_tap_time = now

                # 🔴 BIG RED TAP
                cv2.putText(
                    frame,
                    "TAP",
                    (cx - 40, cy - 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.4,
                    (0, 0, 255),
                    4
                )

                cv2.circle(frame, (cx, cy), 30, (0, 0, 255), 3)

        prev_y = cy

    cv2.putText(
        frame,
        text,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (255, 0, 0),
        3
    )

    cv2.imshow("Tap Detection Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
