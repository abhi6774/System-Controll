import cv2
import mediapipe as mp
from controller import Controller


def check_fingers_touching(hand_landmarks, threshold):
    # Get the landmarks for the finger tips (Indices 4-8)
    fingertips = [hand_landmarks.landmark[mp.solutions.hands.HandLandmark(
        index)] for index in range(4, 9)]

    # Check if the distance between any two fingertips is greater than a threshold
    for i in range(len(fingertips)):
        distanceOfAll = []
        for j in range(i + 1, len(fingertips)):
            distance = abs(fingertips[i].x - fingertips[j].x) + \
                abs(fingertips[i].y - fingertips[j].y)

            if distance > threshold:
                return False

    return True


# Initialize Mediapipe hand tracking
mp_hands = mp.solutions.hands.Hands(
    static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
controller = Controller()

launchPadState = False

while cap.isOpened():
    ret, frame = cap.read()

    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)

    # Convert the BGR frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = mp_hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            response = check_fingers_touching(hand_landmarks, 0.2)
            if response and not launchPadState:
                print("All fingers are touching.")
                controller.open_launchpad()
                launchPadState = True
            elif not response and launchPadState:
                print("Fingers are not touching.")
                controller.close_launchpad()
                launchPadState = False
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
