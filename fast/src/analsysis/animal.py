from keras.models import load_model
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from PIL import Image, ImageOps
import numpy as np
import io
from insightface.app import FaceAnalysis
import cv2
import tensorflow as tf
#from tensorflow.keras.models import load_model

app = FastAPI()

model_path = 'E:/dev/fast/refore-inference/src/analsysis/keras_model.h5'
model = load_model(model_path)
text_path = 'E:/dev/fast/refore-inference/src/analsysis/labels.txt'

class_names = [line.strip() for line in open(text_path, 'r', encoding='utf-8')]

animal_router = APIRouter(prefix="/in")

def get_providers():
    if tf.config.list_physical_devices('GPU'):
        print('GPU 실행')
        providers = ['CUDAExecutionProvider']
    else:
        print('CPU 실행')
        providers = ['CPUExecutionProvider']
    return providers

@animal_router.post("/img")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    providers = get_providers()
    app = FaceAnalysis(providers=providers)
    app.prepare(ctx_id=0, det_size=(640, 640))
    
    faces = app.get(img)
    
    if len(faces) == 0:
        raise HTTPException(status_code=404, detail="이미지에서 얼굴을 인식할 수 없습니다.")
    
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    prediction = model.predict(data)
    
    # 클래스별 확률을 포함한 결과를 생성하고 퍼센트로 변환
    prediction_result = {class_names[i]: "{:.2f}%".format(float(prediction[0][i]) * 100) for i in range(len(class_names))}
    # 결과를 확률에 따라 내림차순으로 정렬
    sorted_prediction = sorted(prediction_result.items(), key=lambda x: float(x[1].rstrip('%')), reverse=True)
    
    return {"predictions": sorted_prediction}

app.include_router(animal_router)
