import streamlit as st
from PIL import Image, ImageDraw # ImageDraw is kept in case you want to add other drawing features later
import numpy as np # Numpy is kept as it's a common dependency, though not strictly needed without easyocr
import io

def extract_text_with_boxes(image):
    # With easyocr removed, this function will now just return the original image
    # and an empty string for the extracted text.
    # If you wish to add a different OCR library later, this is where you'd integrate it.
    
    # Ensure the image is in RGB format for consistent display
    image_rgb = image.convert("RGB")
    
    # No OCR processing is done here.
    extracted_text = "" # No text extracted without an OCR engine
    
    return image_rgb, extracted_text

def main():
    st.set_page_config(page_title="Image Viewer", layout="centered") # Changed title to reflect new functionality
    st.title("Image Viewer") # Changed title
    st.markdown("Upload an image to display it.") # Updated description

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        with st.spinner('Loading image...'): # Updated spinner message
            try:
                image = Image.open(io.BytesIO(uploaded_file.read()))
                
                # Call the modified function; it will now just return the image
                annotated_img, extracted_text = extract_text_with_boxes(image)
                
                st.subheader("Uploaded Image:") # Updated subheader
                st.image(annotated_img, caption="Displayed Image", use_column_width=True)
                
                # Removed the "Extracted Text" section as OCR is no longer performed.
                # If you want to show a message, you can add:
                # st.info("Text extraction functionality is currently disabled.")
                
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
                st.info("Please ensure the uploaded file is a valid image.")

if __name__ == "__main__":
    main()
