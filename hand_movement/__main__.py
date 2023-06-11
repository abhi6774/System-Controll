from hand_tracker import HandGestureDetector
import cv2
from metadata import Position

cap = cv2.VideoCapture(0)
detector = HandGestureDetector(show_numbers=True, debugMode=False)


def onMove(position: Position):
    print("On Move", position)


detector.setOnMove(onMove)

while True:
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = detector.detect(frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    frame = cv2.flip(frame, 1)

    cv2.imshow("Track HandMovement", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
