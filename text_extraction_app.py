from PIL import Image, ImageDraw
import easyocr
import numpy as np
import streamlit as st

def extract_text_with_boxes(image):
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(np.array(image), detail=1)  # Get bbox coordinates
    
    draw = ImageDraw.Draw(image)
    extracted_text = []
    
    for (bbox, text, prob) in results:
        extracted_text.append(text)
        draw.rectangle([tuple(bbox[0]), tuple(bbox[2])], outline="green", width=2)
        draw.text((bbox[0][0], bbox[0][1] - 15), text, fill="green")
    
    return image, " ".join(extracted_text)

def main():
    st.title("Text Extraction from Images")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        annotated_img, text = extract_text_with_boxes(image)
        st.image(annotated_img, caption="Detected Text")
        st.write(text)

if __name__ == "__main__":
    main()
