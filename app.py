import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from face_detector import preprocess_image # 이미지 전처리 함수

MODEL_PATH = "./weights/weights_emotions.hdf5"  # HDF5 (가중치 파일) 모델 경로
model = load_model(MODEL_PATH)  # 구현한 얼굴 표정 예측 모델

application = Flask(__name__)

@application.route('/')
def index():
    return render_template("webcam.html")

@application.route('/light')
def main():
    return render_template("light.html")

@application.route("/predict", methods=["POST"])
def predict():
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # 파일 전처리
        print("전처리 시작")
        preprocessed_image, error = preprocess_image(file)
        print("전처리 완료")
        if preprocessed_image is None:
            return jsonify({"error": error}), 400

        # 예측 및 결과 print
        prediction = model.predict(preprocessed_image)
        print("Prediction result:", prediction)
        pred = np.argmax(prediction)
        emotion = ""
        if(pred == 0): emotion = "angry"
        elif(pred == 1): emotion = "disgust"
        elif(pred == 2): emotion = "fear"
        elif(pred == 3): emotion = "happy"
        elif(pred == 4): emotion = "neutral"
        elif(pred == 5): emotion = "sad"
        elif(pred == 6): emotion = "surprise"
        print("Emotion: ", emotion)

        return jsonify({"emotion": emotion})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)