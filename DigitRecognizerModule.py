import tensorflow as tf
from keras.models import load_model
import numpy as np
import cv2


MODEL = load_model("DigitModel.h5")
def predict_img():
    img = cv2.imread("digit.jpg")
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    final_img = cv2.resize(gray,(28,28),interpolation=cv2.INTER_AREA)
    final_img = tf.keras.utils.normalize(final_img,axis = 1)
    final_img = np.array(final_img).reshape(-1,28,28,1)
    
    
    predict = MODEL.predict(final_img)
    return np.argmax(predict)
