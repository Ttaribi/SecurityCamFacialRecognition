
import cv2


cam = cv2.VideoCapture(2)
while True:
    ret, frame = cam.read()
    cv2.imshow("Webcam Test", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

