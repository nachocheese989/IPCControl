import cv2

STREAM_URL = "http://admin:123456@192.168.1.15:80/videostream.cgi"

def stream():
    cap = cv2.VideoCapture(STREAM_URL)
    while True:
        ret, frame = cap.read()
        width = 1500
        height = 1080
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow('Capturing, Q to quit',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): #click q to stop capturing
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream()