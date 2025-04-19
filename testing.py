"""

Detect three fingers and calculate the distance between them

"""

# import cv2
# import mediapipe as mp

# # Initialize the hand detection model
# mpHands = mp.solutions.hands.Hands()

# mp_hands = mp.solutions.hands
# # Create a video capture object
# cap = cv2.VideoCapture(0)

# while True:
#     # Capture the current frame
#     ret, frame = cap.read()

#     # Convert the frame to RGB format
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Detect hands in the frame
#     results = mpHands.process(rgb_frame)

#     # Check if any hands were detected
#     if results.multi_hand_landmarks:
#         # Iterate through the detected hands
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Check if the pinky finger and thumb are overlapping
#             if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x:
#                 # Track the middle finger, pointing finger and ring finger
#                 middle_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
#                 pointing_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
#                 ring_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x

#                 # Calculate the distance between the middle finger, pointing finger and ring finger
#                 middle_finger_pointing_finger_distance = abs(
#                     middle_finger_x - pointing_finger_x)
#                 middle_finger_ring_finger_distance = abs(
#                     middle_finger_x - ring_finger_x)
#                 pointing_finger_ring_finger_distance = abs(
#                     pointing_finger_x - ring_finger_x)
#                 print(middle_finger_pointing_finger_distance,
#                       middle_finger_ring_finger_distance, pointing_finger_ring_finger_distance)

#                 # Do something with the distances
#                 # For example, you could use them to control a virtual object.
#                 # You could also use them to control a virtual keyboard.

#     # Display the frame
#     cv2.imshow("Frame", frame)

#     # Check if the user pressed the ESC key
#     key = cv2.waitKey(1)
#     if key == 27:
#         break


""" 
Code to detect left and right hand
"""


# Initialize Mediapipe hands module
# import cv2
# import mediapipe as mp
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()

# # Set up video capture
# cap = cv2.VideoCapture(0)

# while True:
#     # Read the video frame
#     ret, frame = cap.read()

#     frame = cv2.flip(frame, 1)

#     # Convert the BGR image to RGB
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Process the frame with Mediapipe hands
#     results = hands.process(frame_rgb)

#     # Check if hands were detected
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Check if it's the left or right hand
#             handedness = results.multi_handedness[0].classification[0].label

#             # Get the landmarks of the hand
#             for landmark in hand_landmarks.landmark:
#                 # Print the landmark positions
#                 print(
#                     f"Hand: {handedness}, X: {landmark.x}, Y: {landmark.y}, Z: {landmark.z}")

#     # Display the frame with hand landmarks
#     cv2.imshow('Hand Landmarks', frame)

#     # Check for 'q' key to quit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture and close all windows
# cap.release()
# cv2.destroyAllWindows()


# Hand finger contact detection


# Function to check if all fingers are touching


# import cv2
# import mediapipe as mp
# import os
# from controller import Controller
# def check_fingers_touching(hand_landmarks, threshold):
#     # Get the landmarks for the finger tips (Indices 4-8)
#     fingertips = [hand_landmarks.landmark[mp.solutions.hands.HandLandmark(
#         index)] for index in range(4, 9)]

#     # Check if the distance between any two fingertips is greater than a threshold
#     for i in range(len(fingertips)):
#         distanceOfAll = []
#         for j in range(i + 1, len(fingertips)):
#             distance = abs(fingertips[i].x - fingertips[j].x) + \
#                 abs(fingertips[i].y - fingertips[j].y)

#             if distance > threshold:
#                 return False

#     return True


# # Initialize Mediapipe hand tracking
# mp_hands = mp.solutions.hands.Hands(
#     static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# # Initialize OpenCV video capture
# cap = cv2.VideoCapture(0)
# controller = Controller()

# while cap.isOpened():
#     ret, frame = cap.read()

#     # Flip the frame horizontally for a mirrored view
#     frame = cv2.flip(frame, 1)

#     # Convert the BGR frame to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Process the frame with Mediapipe
#     results = mp_hands.process(rgb_frame)

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Get hand landmarks and visualize them
#             # ... (You can refer to Mediapipe documentation for this)

#             # Check if fingers are touchsing
#             if check_fingers_touching(hand_landmarks, 0.2):
#                 # All fingers are touching
#                 print("All fingers are touching.")

#             else:
#                 # Fingers are not touching
#                 print("Fingers are not touching.")
#                 controller.close_launchpad()

#     cv2.imshow('Frame', frame)

#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()


# Fist detection


# Function to check if the hand gesture represents a fist


# Constants
# import cv2
# import mediapipe as mp
# MIN_DETECTION_CONFIDENCE = 0.5
# FIST_CONFIDENCE_THRESHOLD = 0.9
# CONSECUTIVE_FRAMES_THRESHOLD = 2

# # Enum for hand states


# class HandState:
#     UNKNOWN = 0
#     FIST = 1

# # Function to check if the hand gesture represents a fist


# def is_fist(hand_landmarks):
#     # Get the landmarks for the fingers (Indices 4-8 for each finger)
#     fingertips = [hand_landmarks.landmark[mp.solutions.hands.HandLandmark(
#         index)] for index in range(4, 21)]

#     # Check if the distance between the base of the palm and fingertips is smaller than a threshold
#     for fingertip in fingertips:
#         distance = abs(fingertip.x - hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].x) + \
#             abs(fingertip.y -
#                 hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].y)
#         if distance > 0.4:
#             return False

#     return True


# # Initialize Mediapipe hand tracking
# mp_hands = mp.solutions.hands.Hands(
#     static_image_mode=False, max_num_hands=1, min_detection_confidence=MIN_DETECTION_CONFIDENCE)

# # Initialize OpenCV video capture
# cap = cv2.VideoCapture(0)

# controller =

# # Initialize variables
# hand_state = HandState.UNKNOWN
# consecutive_frames = 0

# while cap.isOpened():
#     ret, frame = cap.read()

#     # Flip the frame horizontally for a mirrored view
#     frame = cv2.flip(frame, 1)

#     # Convert the BGR frame to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Process the frame with Mediapipe
#     results = mp_hands.process(rgb_frame)

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Check if hand gesture represents a fist
#             # print(hand_landmarks)
#             if is_fist(hand_landmarks):
#                 if hand_state != HandState.FIST:
#                     consecutive_frames += 1
#                     if consecutive_frames >= CONSECUTIVE_FRAMES_THRESHOLD:
#                         # Fist detected
#                         hand_state = HandState.FIST
#                         print("Fist detected.")
#             else:
#                 consecutive_frames = 0
#                 hand_state = HandState.UNKNOWN

#     cv2.imshow('Frame', frame)

#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
