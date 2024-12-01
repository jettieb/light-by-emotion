import numpy as np

# 예측값 색으로 바꾸기
def prediction_to_color(prediction):
    pred = np.argmax(prediction)
    color = ""
    emotion = ""
    if(pred == 0): 
        color = "#0099FF" 
        emotion = "angry" 
    elif(pred == 1): 
        color = "#1B2159"
        emotion = "disgust"
    elif(pred == 2): 
        color = "#F381EB"
        emotion = "fear"
    elif(pred == 3): 
        color = "#F9F871"
        emotion = "happy"
    elif(pred == 4):
        color = "#FFFFFF"
        emotion = "neutral"
    elif(pred == 5): 
        color = "#FF9900"
        emotion = "sad"
    elif(pred == 6): 
        color = "#F0CF2A"
        emotion = "surprise"
    print("Emotion: ", emotion)
    print("Color: ", color)

    return color