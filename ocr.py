import os
import io
from google.cloud import vision

# Google Cloud Vision API 인증 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/yunseo/Desktop/development/smapill/ai_google_ocr/google-cloud-key/pro-gecko-444007-a8-1364f6fccaef.json"

def ocr_process(image_path):
    """
    Google Vision API를 사용하여 OCR 처리.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description  # OCR에서 추출된 전체 텍스트 반환
    return ""
