import os
import io
import json
from flask import Flask, request, jsonify
from ocr import ocr_process, extract_pills_from_text

app = Flask(__name__)

# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = "/Users/yunseo/Desktop/development/smapill/ai_google_ocr/image"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)
    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200


@app.route("/process", methods=["POST"])
def process_image():
    try:
        data = request.get_json()
        image_path = data.get("file_path")

        # OCR 및 알약 추출
        text = ocr_process(image_path)
        if text:
            pills = extract_pills_from_text(text)
            return jsonify({"message": "Success", "pills": pills}), 200
        else:
            return jsonify({"message": "Failed to extract text"}), 500

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Processing failed", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
