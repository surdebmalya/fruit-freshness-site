from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import model_from_json
import joblib
from keras.preprocessing import image
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.multioutput import MultiOutputRegressor

def processing(testing_image_path, loaded_model):
    IMG_SIZE = 224
    img = load_img(testing_image_path, 
            target_size=(IMG_SIZE, IMG_SIZE), color_mode="grayscale")
    img_array = img_to_array(img)
    img_array = img_array.reshape((1, IMG_SIZE, IMG_SIZE, 1)) 
    # img_array = img_array/255.0
    prediction = loaded_model.predict(img_array)
    return prediction

def predicting_classification(image_path):
    model_path_h5 = "model/model_classification.h5"
    model_path_json = "model/model_classification.json"
    json_file = open(model_path_json, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(model_path_h5)
    loaded_model.compile(loss='binary_crossentropy', metrics=['accuracy'],optimizer='rmsprop')
    prediction = processing(image_path, loaded_model)
    value = prediction[0][0]
    # print(value)
    if value>0.5:
        result = 1
    else:
        result = 0
    return result

def predicting_regression(image_path):
    model_path_pkl = "model/finalized_regression_model.pkl"
    loaded_model = joblib.load(model_path_pkl)
    img_width, img_height = 224, 224
    img = image.load_img(image_path, target_size = (img_width, img_height), color_mode="grayscale")
    img = image.img_to_array(img)
    img = img.tolist()
    
    test_X=[]
    for row in range(len(img)):
        for height in range(len(img[0])):
            for col in range(len(img[0][0])):
                test_X.append(img[row][height][col])
    
    temp=[]
    for i in range(img_width*img_height):
        temp.append(str(i))
    columnName = temp
    test_df = pd.DataFrame(columns = columnName)

    test_df.loc[len(test_df.index)] = test_X

    pred = loaded_model.predict(test_df)
    colour_prediction = pred[0][0]
    shape_prediction = pred[0][1]
    texture_prediction = pred[0][2]

    return (colour_prediction, shape_prediction, texture_prediction)
