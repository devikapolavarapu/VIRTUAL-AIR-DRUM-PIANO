import cv2
import mediapipe as mp

# MediaPipe setup
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

# Finger tip landmark IDs
FINGER_TIPS = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

# Camera
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            for tip_id in FINGER_TIPS:
                lm = hand.landmark[tip_id]
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Draw fingertip circle
                cv2.circle(frame, (cx, cy), 12, (0, 255, 0), -1)

    cv2.imshow("Finger Tip Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
