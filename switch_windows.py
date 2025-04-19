import cv2
import mediapipe as mp
from controller import Controller

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1, min_detection_confidence=0.7)


cap = cv2.VideoCapture(0)

controller = Controller()

frame_count_left = 1
frame_count_right = 1

checker = 20

right_clicked = False
left_clicked = False


while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to read video frame")
        break

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)

    results = hands.process(image)

    if results.multi_hand_landmarks:
        # if not right_clicked or not left_clicked:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            pinky_x = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
            pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

            distance = abs(thumb_x - pinky_x) + abs(thumb_y - pinky_y)

            overlap_threshold = 0.2

            if distance < overlap_threshold:
                if thumb_x < pinky_x:
                    frame_count_right += 1
                    if frame_count_right % checker == 0:
                        print("Three-finger movement to the right detected")
                        controller.change_to_right()
                        right_clicked = True
                else:
                    frame_count_left += 1
                    if frame_count_left % checker == 0:
                        print("Three-finger movement to the left detected")
                        controller.change_to_left()
                        left_clicked = True

            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Display the resulting image
    cv2.imshow("Hand Tracking", image)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
