import numpy as np
import cv2
import mss
import pywinctl as pw
import torch

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def capture_app_window(app_title):
    windows = pw.getWindowsWithTitle(app_title)
    if not windows:
        print(f"No windows found with title: {app_title}")
        return

    window = windows[0]

    with mss.mss() as sct:
        monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}

        while True:
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Inference
            results = model(frame)

            # Results
            labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
            n = len(labels)
            for i in range(n):
                row = cord[i]
                x1, y1, x2, y2 = int(row[0]*frame.shape[1]), int(row[1]*frame.shape[0]), int(row[2]*frame.shape[1]), int(row[3]*frame.shape[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = results.names[int(labels[i])]
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow("YOLOv5 Object Detection", frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

def list_window_titles():
    windows = pw.getAllTitles()
    return windows

titles = list_window_titles()
for title in titles:
    print(title)

capture_app_window("DE FPV")
