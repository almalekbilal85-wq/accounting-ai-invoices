import pytesseract
import cv2
import numpy as np

def getOCRtext(imageFile):
    
    # Read file bytes
    file_bytes = np.frombuffer(imageFile.read(), np.uint8)

    # Decode image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # OCR
    text = pytesseract.image_to_string(gray)
    return text

