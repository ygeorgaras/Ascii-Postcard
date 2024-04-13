import cv2
import numpy as np

def applyCannyEdgeDetection(image_path, low_threshold=50, high_threshold=150):
    # Read the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Check if image is loaded properly
    if img is None:
        print("Error: Image could not be read.")
        return None

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img)

    # Apply Bilateral Filter to reduce noise and preserve edges
    img_bilateral = cv2.bilateralFilter(img_clahe, d=9, sigmaColor=75, sigmaSpace=75)

    # Apply Canny edge detection
    edges = cv2.Canny(img_bilateral, low_threshold, high_threshold)
    edges_dilated = cv2.dilate(edges, kernel=np.ones((3,3), np.uint8), iterations=1)

    # Combine original and edges for display
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    edges_color = cv2.cvtColor(edges_dilated, cv2.COLOR_GRAY2BGR)
    combined = np.concatenate((img_color, edges_color), axis=1)

    # Display the combined image
    cv2.imshow('Combined', combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (img, edges_dilated)
