import cv2
import time
import os

width, height = 1080,720

CAMERA_INDEX = 0
video_output = "output.mp4"
frame_output_dir = "saved_frames"
os.makedirs(frame_output_dir, exist_ok=True)

prev_time = time.time()
frame_count = -1

cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter(
    video_output,
    fourcc,
    10,
    (width, height)
)

if not video_writer.isOpened():
    print("Error: Could not open video writer.")
    cap.release()
    exit()

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    frame_count += 1
    elapsed = time.time() - start_time


    current_time = time.time()
    calculated_fps = 1.0 / (current_time - prev_time)
    prev_time = current_time

    cv2.putText(
    frame,
    f"FPS: {calculated_fps:.2f}",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.0,
    (0, 255, 0),
    2,
    cv2.LINE_AA
    )

    # Calculate FPS every 30 frames
    if frame_count % 30 == 0:
        fps = 30 / elapsed
        print(f"FPS: {fps:.2f}")
        start_time = time.time()  # reset timer

    video_writer.write(frame)

    if frame_count % 100 == 0:
        frame_filename = os.path.join(
            frame_output_dir, f"frame_{frame_count:06d}.jpg"
        )
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")
        exec(open(os.path.join(os.path.expanduser('~'),"work","drone","Josh-work","Rocketry","Telemetry.py")).read())
        #exec(open(os.path.join(os.path.expanduser('~'),"work","drone","Rocketry","Metrics_Control.py")).read())

    # Optional: display
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()
