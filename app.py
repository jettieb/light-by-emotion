import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from face_detector import preprocess_image # 이미지 전처리 함수

MODEL_PATH = "./weights/weights_emotions.hdf5"  # HDF5 (가중치 파일) 모델 경로
model = load_model(MODEL_PATH)  # 구현한 얼굴 표정 예측 모델

application = Flask(__name__)

@application.route('/')
def index():
    return render_template("webcam.html")

@application.route("/predict", methods=["POST"])
def predict():
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # 파일 전처리
        preprocessed_image, error = preprocess_image(file)

        if preprocessed_image is None:
            return jsonify({"error": error}), 400

        # 예측 및 결과 print
        prediction = model.predict(preprocessed_image)
        print("Prediction result:", prediction)

        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)