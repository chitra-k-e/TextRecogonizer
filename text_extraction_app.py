import streamlit as st
from PIL import Image, ImageDraw
import easyocr
import numpy as np
import io

def extract_text_with_boxes(image):
    image_rgb = image.convert("RGB")
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(np.array(image_rgb), detail=1)
    draw = ImageDraw.Draw(image_rgb)
    extracted_text_parts = []
    for (bbox, text, prob) in results:
        extracted_text_parts.append(text)
        top_left = tuple(bbox[0])
        bottom_right = tuple(bbox[2])
        draw.rectangle([top_left, bottom_right], outline="green", width=2)
        text_x = bbox[0][0]
        text_y = bbox[0][1] - 20
        if text_y < 0:
            text_y = bbox[0][1] + 5
        try:
            draw.text((text_x, text_y), text, fill="red")
        except Exception:
            draw.text((text_x, text_y), text, fill="red")
    full_extracted_text = " ".join(extracted_text_parts)
    return image_rgb, full_extracted_text

def main():
    st.set_page_config(page_title="Image Text Extractor", layout="centered")
    st.title("Text Extraction from Images")
    st.markdown("Upload an image to extract text and see detected regions.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        with st.spinner('Processing image and extracting text...'):
            try:
                image = Image.open(io.BytesIO(uploaded_file.read()))
                annotated_img, extracted_text = extract_text_with_boxes(image)
                st.subheader("Detected Text Regions:")
                st.image(annotated_img, caption="Image with Detected Text", use_column_width=True)
                st.subheader("Extracted Text:")
                st.write(extracted_text)
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
                st.info("Please ensure the uploaded file is a valid image.")

if __name__ == "__main__":
    main()
