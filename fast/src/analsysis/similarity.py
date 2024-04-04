from fastapi import APIRouter, UploadFile, File, HTTPException
import cv2
import numpy as np
import os
from insightface.app import FaceAnalysis

similarity_router = APIRouter(prefix="/in")

@similarity_router.post("/upimg")
async def upload_img(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        app = FaceAnalysis(providers=['CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        faces = app.get(img)

        # 얼굴상 분류 로직을 추가하세요
        for face in faces:
            bbox = face['bbox'].astype(int)
            # 예를 들어, 얼굴 크기나 비율에 따라 얼굴상을 분류할 수 있습니다.
            # 여기서는 분류 로직을 구현하는 대신 얼굴상을 "미정"으로 설정합니다.
            face_type = "미정"  # 실제 로직으로 대체 필요

            # 분류된 얼굴상에 따라 사각형의 색을 변경할 수 있습니다.
            color = (0, 255, 0) if face_type == "고양이상" else (255, 0, 0) if face_type == "강아지상" else (0, 0, 255)
            img = cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            # 얼굴상 분류 결과를 이미지에 텍스트로 추가할 수도 있습니다.
            cv2.putText(img, face_type, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        output_path = "t1_output.jpg"
        cv2.imwrite(output_path, img)

        return {"message": "이미지 처리가 성공적으로 완료되었습니다.", "output_path": output_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        await file.close()
