from hand_movement.hand_tracker import HandGestureDetector
from controller import Controller
import cv2

cap = cv2.VideoCapture(0)
detector = HandGestureDetector(show_numbers=True, debugMode=False)
controller = Controller()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)


def onMove(movement):
    controller.moveCursor(movement)


def onMove2(movement):
    print("OnMove", movement)


def onTap(position):
    controller.click()
    print("OnTap", position)


detector.setOnMove(onMove)
detector.setOnMove(onMove2)

detector.setOnTap(onTap)

frame_counts = 0
if __name__ == "__main__":
    while True:
        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        # if frame_counts % 5 == 0:
        frame = detector.detect(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_counts += 1
        cv2.imshow("Track HandMovement", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
