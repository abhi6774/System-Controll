import cv2
import time
import multiprocessing as mpp
import mediapipe as mp

# Define the worker function for OpenCV2 UI


def opencv_worker(frame_queue, fps):
    cv2.namedWindow("OpenCV2 UI", cv2.WINDOW_NORMAL)
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            cv2.putText(frame, f"FPS: {fps.value:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("OpenCV2 UI", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

# Define the worker function for MediaPipe data processing


def mediapipe_worker(frame_queue):
    drawing = mp.solutions.drawing_utils
    hands = mp.solutions.hands

    with hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hand_detector:
        while True:
            if not frame_queue.empty():
                frame = frame_queue.get()
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hand_detector.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        drawing.draw_landmarks(
                            image, hand_landmarks, hands.HAND_CONNECTIONS)
                cv2.putText(image, f"FPS: {fps.value:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('MediaPipe Data Processing', image)

            if cv2.waitKey(1) == ord('q'):
                break
    cv2.destroyAllWindows()

# Define the main function


frame_queue = mpp.Queue()
fps = mpp.Value('d', 0.0)


def main():

    # Create and start the OpenCV2 UI worker process
    opencv_process = mpp.Process(target=opencv_worker, args=(frame_queue, fps))
    opencv_process.start()

    # Create and start the MediaPipe data processing worker process
    mediapipe_process = mpp.Process(
        target=mediapipe_worker, args=(frame_queue,))
    mediapipe_process.start()

    # Read video frames and put them into the frame queue
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_fps = frame_count / elapsed_time
        fps.value = current_fps
        frame_queue.put(frame)

        if cv2.waitKey(1) == ord('q'):
            cap.release()
            break

    # Wait for the processes to finish
    opencv_process.terminate()
    mediapipe_process.terminate()
    opencv_process.join()
    mediapipe_process.join()


if __name__ == '__main__':
    main()
