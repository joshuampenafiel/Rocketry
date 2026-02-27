import cv2
import time
import os

#
# # Set camera index (usually 0 for first USB camera)
camera_index = 0
#
# # Desired resolution
width, height = 1080,720

video_output = "output.mp4"
frame_output_dir = "saved_frames"
os.makedirs(frame_output_dir, exist_ok=True)

# Open the camera
cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MPJG'))
#cap.set(cv2.CAP_PROP_EXPOSURE,0.00000000001)
#cap.set(cv2.CAP_PROP_BRIGHTNESS,50)
#cap.set(cv2.CAP_PROP_GAIN,.01)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

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

print("Press 'q' to quit.")
#
prev_time = time.time()
frame_count = -1

while True:
    start_time = time.time()

    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame_count += 1

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

    # Display the resulting frame
    cv2.imshow('USB Camera', frame)

    video_writer.write(frame)

    if frame_count % 100 == 0:
        frame_filename = os.path.join(
            frame_output_dir, f"frame_{frame_count:06d}.jpg"
        )
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")
        exec(open(os.path.join(os.path.expanduser('~'),"work","drone","Josh-work","Rocketry","Telemetry.py")).read())
        exec(open(os.path.join(os.path.expanduser('~'),"work","drone","Josh-work","Rocketry","Metrics_Control.py")).read())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
video_writer.release()
cv2.destroyAllWindows()
