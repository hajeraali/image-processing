import cv2
import os

def process_image(filepath, operation, value, output_folder):
    image = cv2.imread(filepath)
    
    if operation == 'blur':
        ksize = int(value)
        processed_image = cv2.GaussianBlur(image, (ksize, ksize), 0)
    
    elif operation == 'contrast':
        alpha = float(value)
        processed_image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)
    
    elif operation == 'sharpen':
        kernel_size = int(value)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        processed_image = cv2.filter2D(image, -1, kernel)
    
    output_filename = f"{operation}_{os.path.basename(filepath)}"
    output_path = os.path.join(output_folder, output_filename)
    cv2.imwrite(output_path, processed_image)
    
    return output_filename
