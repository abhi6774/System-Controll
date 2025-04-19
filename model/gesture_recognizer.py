import mediapipe as mp
import cv2
from controller import Controller

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

controller = Controller()

options = GestureRecognizerOptions(
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
    base_options=BaseOptions(
        model_asset_path='./model/gesture_recognizer.task'),
    running_mode=VisionRunningMode.IMAGE)

with GestureRecognizer.create_from_options(options) as recognizer:
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection = recognizer.recognize(mp_image)
        print(detection)
        if detection.gestures.__len__() > 0:
            print(
                "-----------------------------------------------------------------------")
            print(detection.gestures[0][0].category_name)
            if (detection.gestures[0][0].category_name == "Closed_Fist"):
                controller.open_launchpad()

            elif detection.gestures[0][0].category_name == "Open_Palm":
                controller.close_launchpad()
            print(
                "-----------------------------------------------------------------------")
        cv2.imshow("Gesture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
