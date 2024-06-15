import cv2
import sys

# Inisialisasi classifier untuk deteksi wajah, mata, dan mulut
mouthCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Membuka video capture dari kamera default
video_capture = cv2.VideoCapture(0)

while True:
    # Membaca frame dari video
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Mengkonversi gambar ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteksi wajah
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Loop melalui setiap wajah yang terdeteksi
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, 'wajah', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Region of Interest untuk mulut dan mata
        roi_gray_mouth = gray[y + h//2:y+h, x:x+w]
        roi_color_mouth = frame[y + h//2:y+h, x:x+w]
        roi_gray_eye = gray[y:y + h//2, x:x+w]
        roi_color_eye = frame[y:y + h//2, x:x+w]

        # Deteksi mulut dan mata dalam ROI
        mouths = mouthCascade.detectMultiScale(roi_gray_mouth, scaleFactor=1.5, minNeighbors=5)
        eyes = eyeCascade.detectMultiScale(roi_gray_eye, scaleFactor=1.1, minNeighbors=10)

        for (mx, my, mw, mh) in mouths:
            cv2.rectangle(roi_color_mouth, (mx, my), (mx+mw, my+mh), (0, 255, 0), 2)

        for (ex, ey, ew, eh) in eyes:
            cv2.circle(roi_color_eye, (ex + ew//2, ey + eh//2), ew//2, (0, 0, 255), 2)

    # Menampilkan frame yang sudah diproses
    cv2.imshow('Video', frame)

    # Keluar loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan video capture dan menutup semua window
video_capture.release()
cv2.destroyAllWindows()
