import cv2
import mediapipe as mp
import numpy as np

# Inisialisasi MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Canvas untuk menggambar
canvas = None

# Posisi terakhir jari telunjuk
last_index_finger_position = None

# Fungsi untuk mengecek apakah jari tertentu terangkat
def is_finger_up(hand_landmarks, finger_tip_idx, finger_dip_idx):
    if finger_tip_idx < len(hand_landmarks.landmark) and finger_dip_idx < len(hand_landmarks.landmark):
        tip = np.array([hand_landmarks.landmark[finger_tip_idx].x, hand_landmarks.landmark[finger_tip_idx].y])
        dip = np.array([hand_landmarks.landmark[finger_dip_idx].x, hand_landmarks.landmark[finger_dip_idx].y])
        return tip[1] < dip[1]
    return False

# Fungsi untuk menghapus dengan gesture
def can_erase(hand_landmarks):
    fingers = [mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    if all(i < len(hand_landmarks.landmark) for i in fingers):
        all_up = all(is_finger_up(hand_landmarks, finger, finger + 2) for finger in fingers)
        all_moving = all(hand_landmarks.landmark[finger].y < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y for finger in fingers)
        return all_up and all_moving
    return False

# Capture video dari webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Flip frame untuk mirror view
    frame = cv2.flip(frame, 1)

    # Proses deteksi tangan
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Gambar landmarks di tangan
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
            
            # Menulis hanya jika jari telunjuk terangkat
            if is_finger_up(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_DIP):
                if last_index_finger_position is not None:
                    cv2.line(canvas, last_index_finger_position, (index_x, index_y), (0, 0, 255), 5)
                last_index_finger_position = (index_x, index_y)
            else:
                last_index_finger_position = None

            # Menghapus dengan melambaikan jari tengah, manis, dan kelingking
            if can_erase(hand_landmarks):
                canvas = np.zeros_like(frame)

    # Gabungkan canvas dengan frame
    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
