import cv2
import os
import numpy as np

def process_image(filepath, operation, value, output_folder):
    image = cv2.imread(filepath)
    
    if operation == 'blur':
        ksize = int(value)
        if ksize % 2 == 0:  # Ensure the kernel size is odd
            ksize += 1
        processed_image = cv2.GaussianBlur(image, (ksize, ksize), 0)
    
    elif operation == 'contrast':
        alpha = float(value)
        beta = 1  # You can adjust this value if needed
        processed_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    elif operation == 'sharpen':
        kernel_size = int(value)
        if kernel_size % 2 == 0:
            kernel_size += 1
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # Simple sharpen kernel
        processed_image = cv2.filter2D(image, -1, kernel)

    elif operation == 'invert':
        # Assume the mask is a single-channel binary image
        mask = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)  # Convert to binary mask
        processed_image = cv2.bitwise_not(mask)  # Invert the mask

    elif operation == 'detect_white':
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Threshold to find white regions
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours on original image (copy)
        processed_image = image.copy()
        cv2.drawContours(processed_image, contours, -1, (0, 0, 255), 2)  # Draw red contours
    
    else:
        return None
    
    output_filename = f"{operation}_{os.path.basename(filepath)}"
    output_path = os.path.join(output_folder, output_filename)
    cv2.imwrite(output_path, processed_image)
    
    return output_filename
