import cv2
import numpy as np

def applyCannyEdgeDetection(image_path, low_threshold=50, high_threshold=150):
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if image is loaded properly
    if img is None:
        print("Error: Image could not be read.")
        return None

    # Apply Gaussian Blur to reduce noise and improve edge detection
    img_blurred = cv2.GaussianBlur(img, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(img_blurred, low_threshold, high_threshold)

    return edges
