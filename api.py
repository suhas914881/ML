import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import io


# create API
app = FastAPI()


# allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# load trained model
model = tf.keras.models.load_model("best_arecanut_model.h5")


# class names (must match training folders)
classes = [
"Healthy_Leaf",
"Healthy_Nut",
"Healthy_Trunk",
"Mahali_Koleroga",
"yellow_leaf_disease"
]


# disease descriptions
descriptions = {

"Healthy_Leaf":{
"en":
"Leaf is healthy. Plant is growing properly with sufficient nutrients.",

"kn":
"ಎಲೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ. ಸಸ್ಯ ಸರಿಯಾಗಿ ಬೆಳೆಯುತ್ತಿದೆ."
},

"Healthy_Nut":{
"en":
"Nut is healthy with good quality and proper growth.",

"kn":
"ಅಡಿಕೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ ಮತ್ತು ಸರಿಯಾಗಿ ಬೆಳೆಯುತ್ತಿದೆ."
},

"Healthy_Trunk":{
"en":
"Trunk is strong and disease free.",

"kn":
"ಕಾಂಡ ಆರೋಗ್ಯಕರವಾಗಿದೆ ಮತ್ತು ಯಾವುದೇ ರೋಗ ಇಲ್ಲ."
},

"Mahali_Koleroga":{
"en":
"Mahali disease is a fungal infection occurring in rainy season.\nIt causes rotting of arecanut and reduces yield.",

"kn":
"ಮಹಾಳಿ ರೋಗವು ಮಳೆಯ ಸಮಯದಲ್ಲಿ ಉಂಟಾಗುವ ಶಿಲೀಂಧ್ರ ರೋಗ.\nಇದು ಅಡಿಕೆಯನ್ನು ಹಾಳುಮಾಡುತ್ತದೆ."
},

"yellow_leaf_disease":{
"en":
"Yellow leaf disease occurs due to nutrient deficiency.\nLeaves become yellow and plant growth reduces.",

"kn":
"ಪೋಷಕಾಂಶ ಕೊರತೆಯಿಂದ ಎಲೆ ಹಳದಿ ಬಣ್ಣವಾಗುತ್ತದೆ.\nಸಸ್ಯ ಬೆಳವಣಿಗೆ ಕಡಿಮೆಯಾಗುತ್ತದೆ."
}

}


# precautions
precautions = {

"Healthy_Leaf":{
"en":
"Maintain irrigation regularly and monitor plant growth.",

"kn":
"ನೀರಾವರಿ ಸರಿಯಾಗಿ ಮಾಡಿ ಮತ್ತು ಸಸ್ಯವನ್ನು ಗಮನಿಸಿ."
},

"Healthy_Nut":{
"en":
"Keep soil nutrients balanced and avoid excess moisture.",

"kn":
"ಮಣ್ಣಿನ ಪೋಷಕಾಂಶ ಸಮತೋಲನ ಕಾಪಾಡಿ."
},

"Healthy_Trunk":{
"en":
"Protect trunk from physical damage and pests.",

"kn":
"ಕಾಂಡಕ್ಕೆ ಹಾನಿಯಾಗದಂತೆ ನೋಡಿಕೊಳ್ಳಿ."
},

"Mahali_Koleroga":{
"en":
"Avoid excess water stagnation.\nRemove infected nuts early.",

"kn":
"ಹೆಚ್ಚು ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.\nಸೋಂಕಿತ ಅಡಿಕೆ ತೆಗೆದುಹಾಕಿ."
},

"yellow_leaf_disease":{
"en":
"Check soil nutrients and improve drainage.",

"kn":
"ಮಣ್ಣಿನ ಪೋಷಕಾಂಶ ಪರಿಶೀಲಿಸಿ ಮತ್ತು ನೀರಿನ ಹರಿವು ಸುಧಾರಿಸಿ."
}

}


# solutions (2–3 lines)
solutions = {

"Healthy_Leaf":{
"en":
"Plant is healthy.\nApply organic manure and NPK fertilizer regularly.",

"kn":
"ಸಸ್ಯ ಆರೋಗ್ಯಕರವಾಗಿದೆ.\nಜೈವಿಕ ಗೊಬ್ಬರ ಮತ್ತು NPK ಗೊಬ್ಬರ ಬಳಸಿ."
},

"Healthy_Nut":{
"en":
"Nut is healthy.\nMaintain balanced fertilizer and proper irrigation.",

"kn":
"ಅಡಿಕೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ.\nಸಮತೋಲನ ಗೊಬ್ಬರ ಮತ್ತು ನೀರಾವರಿ ಬಳಸಿ."
},

"Healthy_Trunk":{
"en":
"Plant trunk is healthy.\nApply compost and protect from pests.",

"kn":
"ಕಾಂಡ ಆರೋಗ್ಯಕರವಾಗಿದೆ.\nಜೈವಿಕ ಗೊಬ್ಬರ ಬಳಸಿ."
},

"Mahali_Koleroga":{
"en":
"Spray Bordeaux mixture (1%) or Copper fungicide.\nRepeat spray every 15 days in rainy season.",

"kn":
"ಬೋರ್ಡೋ ಮಿಶ್ರಣ ಅಥವಾ ಕಾಪರ್ ಔಷಧಿ ಸಿಂಪಡಿಸಿ.\n15 ದಿನಕ್ಕೊಮ್ಮೆ ಸಿಂಪಡಿಸಿ."
},

"yellow_leaf_disease":{
"en":
"Apply NPK fertilizer and Magnesium Sulphate.\nImprove soil drainage and nutrient balance.",

"kn":
"NPK ಗೊಬ್ಬರ ಮತ್ತು ಮ್ಯಾಗ್ನೀಷಿಯಂ ಸಲ್ಫೇಟ್ ಬಳಸಿ.\nನೀರಿನ ಹರಿವು ಸುಧಾರಿಸಿ."
}

}


# home route
@app.get("/")
def home():

    return {"message":"Arecanut Disease Detection API running"}

# prediction route
@app.post("/predict")

async def predict(file: UploadFile = File(...), lang: str="en"):
    # read image
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))
    # resize same as training
    img = img.resize((160,160))
    # preprocessing
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    # prediction
    prediction = model.predict(img_array)
    predicted_class = classes[np.argmax(prediction)]
    confidence = float(np.max(prediction))*100
    # return result
    return {

    "class": predicted_class,

    "confidence": round(confidence,2),

    "description": descriptions[predicted_class][lang],

    "precaution": precautions[predicted_class][lang],

    "solution": solutions[predicted_class][lang]

    }