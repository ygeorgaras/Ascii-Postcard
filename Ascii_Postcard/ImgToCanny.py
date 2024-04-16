import cv2
import numpy as np

def applyCannyEdgeDetection(imagePath, lowThreshold=50, highThreshold=150):
    # Read the image in grayscale
    img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    
    # Check if image is loaded properly
    if img is None:
        print("Error: Image could not be read.")
        return None

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    imgClahe = clahe.apply(img)

    # Apply Bilateral Filter to reduce noise and preserve edges
    imgBilateral = cv2.bilateralFilter(imgClahe, d=9, sigmaColor=75, sigmaSpace=75)

    # Apply Canny edge detection
    edges = cv2.Canny(imgBilateral, lowThreshold, highThreshold)
    edgesDilated = cv2.dilate(edges, kernel=np.ones((1,1), np.uint8), iterations=1)

    # Combine original and edges for display
    imgColor = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    edgesColor = cv2.cvtColor(edgesDilated, cv2.COLOR_GRAY2BGR)
    combined = np.concatenate((imgColor, edgesColor), axis=1)

    # Display the combined image
    cv2.imshow('Combined', combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return np.uint8(edgesDilated)
