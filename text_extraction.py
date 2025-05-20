from PIL import Image, ImageDraw
import pytesseract
import streamlit as st
import numpy as np

def extract_text_with_boxes(image):
    # Use pytesseract instead of easyocr
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    draw = ImageDraw.Draw(image)
    extracted_text = []
    
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:  # Confidence threshold
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            text = data['text'][i]
            extracted_text.append(text)
            draw.rectangle([x, y, x+w, y+h], outline="green", width=2)
            draw.text((x, y-15), text, fill="green")
    
    return image, " ".join(extracted_text)
if __name__ == "__main__":
    main()
