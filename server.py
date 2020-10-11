import requests
import config
import boto3
import face
from typing import List
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
client = boto3.client('rekognition')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return "OK"

@app.post("/api/user/image/")
async def register_face(request: Request, file: UploadFile = File(...)):
    if 'bearer-token' not in request.headers or 'gauth-token' not in request.headers:
        raise HTTPException(401, "unauthorized")

    img_str = await file.read()
    face_detected = await face.detect(img_str)
    if not face_detected:
        raise HTTPException(400, "face not detected")

    files = {'file': bytes(img_str)}
    headers = {
        'bearer-token': request.headers['bearer-token'],
        'gauth-token': request.headers['gauth-token']
    }
    response = requests.post("http://" + "localhost:8002" + "/api/user/image/", files=files, headers=headers)
    if not response.status_code == 200 and not response.status_code == 201:
        raise HTTPException(response.status_code, response.reason)

    body = response.json()
    if "data" not in body:
        raise HTTPException(500, "something went wrong")

    return {
        "filename": file.filename,
        "face_detected": face_detected,
        "data": body["data"]
    }

@app.post("/verify/{user_id}")
async def register_face(request: Request, user_id, files: List[UploadFile] = File(...)):
    if 'bearer-token' not in request.headers or 'gauth-token' not in request.headers:
        raise HTTPException(401, "unauthorized")

    if len(files) < 5:
        raise HTTPException(400, "insufficient uploaded image(s)")

    detected = 0
    img_bytestr = None
    for file in files:
        img_str = await file.read()
        face_detected = await face.detect(img_str)
        if face_detected:
            img_bytestr = img_str
            detected += 1

    if detected < 3 or img_bytestr is None:
        raise HTTPException(400, "failed to verify liveness")

    url = "http://" + config.AUTH_SERVICE_ADDR + "/api/user/" + str(user_id)

    response = requests.get(url)
    if not response.status_code == 200 and not response.status_code == 201:
        raise HTTPException(response.status_code, response.reason)

    body = response.json()
    result = face.compare(body['image_path'], bytes(img_bytestr), client)

    if not result:
        raise HTTPException(400, "failed to verify face")

    return "face verified"

def main():
    # Replace sourceFile and targetFile with the image files you want to compare.
    source_file = 'face1.jpg'
    target_file = 'face2.jpg'

    source_file = open(source_file, 'rb')
    target_file = open(target_file, 'rb')

    same = face.compare(source_file.read(), target_file.read(), client)
    if same:
        print("OK")
    else:
        print("NOT OK")

    source_file.close()
    target_file.close()
