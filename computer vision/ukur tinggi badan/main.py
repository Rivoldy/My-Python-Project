import cv2
import torch
import numpy as np

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def detect_person(frame):
    results = model(frame)
    labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    return labels, cords

def draw_boxes(frame, labels, cords, threshold=0.5):
    height, width = frame.shape[:2]
    for i in range(len(labels)):
        if labels[i] == 0 and cords[i][4] >= threshold:  # 0 is the label for 'person'
            x1, y1, x2, y2 = int(cords[i][0] * width), int(cords[i][1] * height), int(cords[i][2] * width), int(cords[i][3] * height)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            return (x1, y1, x2, y2)
    return None

def calculate_height(person_box, reference_height, reference_pixels):
    x1, y1, x2, y2 = person_box
    person_height_pixels = y2 - y1
    scale_factor = reference_height / reference_pixels
    person_height_real = person_height_pixels * scale_factor
    return person_height_real

# Main function
def main():
    reference_height = 1.7  # meter (assumed height of reference object)
    reference_pixels = 100  # pixels (height of reference object in image)

    cap = cv2.VideoCapture(0)  # Open webcam

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        labels, cords = detect_person(frame)
        person_box = draw_boxes(frame, labels, cords)

        if person_box:
            person_height = calculate_height(person_box, reference_height, reference_pixels)
            x1, y1, x2, y2 = person_box
            cv2.putText(frame, f'Height: {person_height:.2f} m', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
