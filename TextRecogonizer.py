
import streamlit as st
import cv2
import easyocr
import numpy as np
from PIL import Image
import tempfile
import os

def extract_text(image):
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image, detail=1)

    extracted_text = ""
    confidence_scores = []

    for (bbox, text, score) in results:
        extracted_text += f"{text} "
        confidence_scores.append(score)
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image, text, (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    avg_conf = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
    return image, extracted_text.strip(), avg_conf

st.set_page_config(page_title="OCR with EasyOCR", layout="centered")

st.title("🔍 Text Extraction from Images (EasyOCR)")

uploaded_files = st.file_uploader("Upload image(s)", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

if uploaded_files:
    highest_conf = 0
    best_image = None
    best_text = ""

    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.read())
            img_path = tmp_file.name

        image = cv2.imread(img_path)
        processed_img, text, conf = extract_text(image)

        if conf > highest_conf:
            highest_conf = conf
            best_image = processed_img
            best_text = text

    if best_image is not None:
        st.image(cv2.cvtColor(best_image, cv2.COLOR_BGR2RGB), caption=f"Confidence: {highest_conf:.2%}")
        st.subheader("Extracted Text:")
        st.write(best_text)

