import cv2
import faceDetector as FD
def readCamera():
    screen = cv2.VideoCapture(0)
    while(True):
        ret, frame = screen.read()
    
        cv2.imshow('Camera Capture', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break
    screen.release()
    cv2.destroyAllWindows()
    return frame

def showFace(f):
    F = FD.detectFace(f)
    if F:
        return True
    return False



