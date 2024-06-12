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
        beta = 2  # You can adjust this value if needed
        processed_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    elif operation == 'sharpen':
        kernel_size = int(value)
        if kernel_size % 2 == 0:
            kernel_size += 1
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # Simple sharpen kernel
        processed_image = cv2.filter2D(image, -1, kernel)
    
    output_filename = f"{operation}_{os.path.basename(filepath)}"
    output_path = os.path.join(output_folder, output_filename)
    cv2.imwrite(output_path, processed_image)
    
    return output_filename
