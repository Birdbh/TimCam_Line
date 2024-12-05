import cv2
import time
import numpy as np
from cv2 import dnn_superres
#from super_image import EdsrModel, ImageLoader
import requests
import db

# Load the pre-trained Haar cascade classifier for pedestrian detection
pedestrian_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel("EDSR_x4.pb")
sr.setModel("edsr", 4)

#model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=2)

POINT1 = (400, 260)
POINT2 = (730, 600)

# URL of the video stream
video_url = "https://streamserve.ok.ubc.ca/LiveCams/timcam.stream_720p/playlist.m3u8"

def openStream():
    # Open the video stream
    cap = cv2.VideoCapture(video_url)

    # Check if the video stream is opened successfully
    if not cap.isOpened():
        print("Error: Could not open the video stream.")
        exit()

    return cap

def readFrame(cap):
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print("Error: Could not read frame.")
        exit()

    return frame

def processFrame(frame):

    # Convert frame to grayscale (required by Haar cascade)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Enhance contrast using histogram equalization
    enhanced_gray = cv2.equalizeHist(gray)

    cropped_enhanced_gray = enhanced_gray[POINT1[1]:POINT2[1], POINT1[0]:POINT2[0]]

    # Create the sharpening kernel 
    # kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 

    # sharpened_cropped_enhanced_gray = cv2.GaussianBlur(cropped_enhanced_gray, (7, 7), 0)


    #upscale = sr.upsample(frame) 

    # cv2.imshow('Frame2', upscale)

    # return upscale

def processFrame1(frame):
    """
    Method 1: Histogram Equalization and Gaussian Blur
    Enhances contrast and reduces noise
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply histogram equalization to improve contrast
    equalized = cv2.equalizeHist(gray)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
    
    return blurred

def processFrame2(frame):
    """
    Method 2: Color Space Conversion and Adaptive Thresholding
    Helps in extracting potential pedestrian regions
    """
    # Convert to LAB color space (useful for contrast)
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    # Split channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    # Merge channels back
    lab_improved = cv2.merge((cl, a, b))
    
    # Convert back to BGR
    improved_frame = cv2.cvtColor(lab_improved, cv2.COLOR_LAB2BGR)
    
    # Convert to grayscale for further processing
    gray = cv2.cvtColor(improved_frame, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    return adaptive_thresh

def detectPedestrians(enhanced_frame):

    # Detect pedestrians in the enhanced grayscale frame
    #pedestrians = pedestrian_cascade.detectMultiScale(enhanced_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    pedestrians, _ = hog.detectMultiScale(enhanced_frame, winStride=(4, 4), padding=(4, 4), scale=1.05)

    return pedestrians

def processView(frame, pedestrians):
    # Draw squares around detected pedestrians
    for (x, y, w, h) in pedestrians:
        cv2.rectangle(frame, (x+POINT1[0], y+POINT1[1]), (x+w+POINT1[0], y+h+POINT1[1]), (0, 255, 0), 2)

    cv2.rectangle(frame, POINT1, POINT2, (0, 255, 255), 4)

    # Display the enhanced frame with detected pedestrians
    cv2.imshow('Frame', frame)

    return


def main():
    cap = openStream()

    while True:
        frame = readFrame(cap)
        enhanced_frame = processFrame1(frame)
        cv2.imshow('Frame1', enhanced_frame)
        pedestrians = detectPedestrians(enhanced_frame)
        processView(frame, pedestrians)

        db.insert_data((len(pedestrians),))

        # Wait for 'q' key to exit the loop
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
        time.sleep(0.1)


    # Release the video stream and close any open windows
    cap.release()
    cv2.destroyAllWindows()

main()
