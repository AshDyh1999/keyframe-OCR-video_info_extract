import cv2
cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    cv2.imshow('Video',frame)
    c = cv2.waitKey(1)
    if c == 27:
        break
cap.release()
cv2.destroyAllWindows()