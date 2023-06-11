import mediapipe as mp
import cv2
from hand_movement.metadata import Position
import time


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


class HandGestureDetector:

    __observers = []
    __move_observers = []
    __on_tap_observers = []

    _moveThreshold = 7
    _tapThreshold = 20

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.7, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    WRIST_X_CHANGE = 0
    WRIST_Y_CHANGE = 0

    _ptime = 0
    _ctime = 0

    previous_position = {}

    current_position = {}

    def setObservers(self, observer):
        self.__observers.append(observer)

    def showIndexNumbers(self, frame, hand_landmarks):
        for index, landmark in enumerate(hand_landmarks):
            cx, cy = int(
                landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            cv2.putText(frame, str(index), (cx, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def setOnMove(self, func):
        self.__move_observers.append(func)

    def setOnTap(self, func):
        self.__on_tap_observers.append(func)

    def debugPrint(self, *args, debugMode=False):
        print(args) if self.debugMode or debugMode else None

    def setCurrentPoint(self, landmarks, frame):
        landmarksId = {
            landmarkId.name: landmarkId.value for landmarkId in self.mp_hands.HandLandmark}

        self.previous_position = self.current_position
        self .current_position = {}
        # if landmarks:
        #     self.current_position = { x: 0 for x in self.current_position.keys()}
        #     return
        if landmarks:
            for key in landmarksId.keys():
                self.current_position[key] = Position(
                    int(landmarks[landmarksId[key]].x * frame.shape[1]),
                    int(landmarks[landmarksId[key]].y * frame.shape[0]))

        else:
            self.current_position = {}
        self.debugPrint(self.current_position)

    def _callOnMoveObservers(self, event: Position):
        for functions in self.__move_observers:
            functions(event)

    def _callOnTabObservers(self, event):
        for functions in self.__on_tap_observers:
            functions(event)

    def _detectForTap(self):
        indexTip = "INDEX_FINGER_TIP"
        wrist_x = self.current_position["WRIST"].x - \
            self.previous_position["WRIST"].y

        x = self.current_position[indexTip].x - \
            self.previous_position[indexTip].x
        y = self.current_position[indexTip].y - \
            self.previous_position[indexTip].y

        # if wrist_x < self._moveThreshold:
        if abs(y) > self._tapThreshold:
            self._callOnTabObservers(Position(x, y))
            return True

        return False

    def _detectForMove(self):
        x = self.current_position["WRIST"].x - \
            self.previous_position["WRIST"].x
        y = self.current_position["WRIST"].y - \
            self.previous_position["WRIST"].y

        self.debugPrint("OnMove Event Occured")

        self.debugPrint(self.current_position["WRIST"].x,
                        self.previous_position["WRIST"].x)
        self.debugPrint(self.current_position["WRIST"].y,
                        self.previous_position["WRIST"].y)
        self.debugPrint(self.WRIST_X_CHANGE,
                        self.WRIST_Y_CHANGE, debugMode=True)
        self.debugPrint(
            "\n----------------------------------------------------\n")
        self.WRIST_X_CHANGE += abs(x)
        self.WRIST_Y_CHANGE += abs(y)

        if int(self.WRIST_X_CHANGE / self._moveThreshold) > 2 or int(self.WRIST_Y_CHANGE / self._moveThreshold) > 2:
            self._callOnMoveObservers(Position(x, y))
            self.WRIST_X_CHANGE = 0
            self.WRIST_Y_CHANGE = 0
            return True
        return False

    def _detectForOpenPalm(self, frame) -> bool:
        options = GestureRecognizerOptions(
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            base_options=BaseOptions(
                model_asset_path='./models/gesture_recognizer.task'),
            running_mode=VisionRunningMode.IMAGE)
        with GestureRecognizer.create_from_options(options) as recognizer:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            detection = recognizer.recognize(mp_image)
            if detection.gestures.__len__() > 0:
                if detection.gestures[0][0].category_name == "Open_Palm":
                    return True

        return False

    def detect(self, frame):
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                                               self.mp_drawing.DrawingSpec(
                                                   color=(0, 255, 0), thickness=2, circle_radius=2),
                                               self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))

                self.setCurrentPoint(hand_landmarks.landmark, frame)

                self.showIndexNumbers(
                    frame, hand_landmarks.landmark) if self.show_numbers else None
        else:
            self.setCurrentPoint(None, frame)

        if self.previous_position and self.current_position:
            if self.previous_position.__len__() > 0 and self.current_position.__len__() > 0:

                self._detectForTap() if not self._detectForMove() else None

        # Displaying FPS

        if self.showFPS:
            self._ctime = time.time()
            fps = 1/(self._ctime - self._ptime)
            self._ptime = self._ctime
            cv2.putText(frame, str(int(fps)), (10, 70),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)

        return frame

    def __init__(self, show_numbers: bool = False, debugMode: bool = False, showFPS: bool = True) -> None:
        self.show_numbers = show_numbers
        self.debugMode = debugMode
        self.showFPS = showFPS
