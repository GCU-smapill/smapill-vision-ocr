from flask import Flask, request, jsonify
import os

app = Flask(__name__)


# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = '/Users/yunseo/Desktop/development/smapill/ai_google_ocr/image'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    # 파일이 요청에 포함되어 있는지 확인
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # 파일 이름이 없는 경우
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # 파일 저장
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200


@app.route('/api/process', methods=['POST'])
def process_data():
    """
    클라이언트에서 JSON 데이터를 수신하고 처리.
    """
    try:
        # JSON 데이터 수신
        data = request.get_json()
        print("Received Data:", data)

        # 서버에서 추가 처리 로직 가능 (현재는 데이터 그대로 반환)
        processed_data = data

        return jsonify({"message": "Data processed successfully", "processed_data": processed_data}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Failed to process data"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
