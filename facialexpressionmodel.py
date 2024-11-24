import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import dlib


MODEL_PATH = "./weights_emotions.hdf5"
#HDF5 (가중치 파일) 모델 경로

FACE_DETECTOR_PATH = "./mmod_human_face_detector.dat"
#mmod 파일

model = load_model(MODEL_PATH)


#face_detector 얼굴 감지기 로드
face_detector = dlib.cnn_face_detection_model_v1(FACE_DETECTOR_PATH)

#이미지 전처리 함수
# 웹캠에서 보내오는 이미지가 바이너리 파일 형태로 전송할 경우로 가정합니다!
def preprocess_image(file) :
    try:
        # 파일에서 이미지 읽기
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # 얼굴 감지
        detection = face_detector(image, 1)
        if len(detection) == 0:
            return None, "얼굴을 감지할 수 없습니다."
        
        # 첫 번째 얼굴 ROI 추출
        left, top, right, bottom = detection[0].rect.left(), detection[0].rect.top(), detection[0].rect.right(), detection[0].rect.bottom()
        roi = image[top:bottom, left:right]

        # ROI 리사이즈 및 정규화
        roi = cv2.resize(roi, (48, 48))
        roi = roi / 255.0
        roi = np.expand_dims(roi, axis=0)  # 배치 차원 추가
        return roi, None
    except Exception as e:
        return None, str(e)