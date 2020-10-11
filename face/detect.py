import numpy as np
import cv2
from fastapi import UploadFile
import face.detection

from config import config


async def detect(img_str) -> bool:
    np_arr = np.fromstring(img_str, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if face.detection.detect(img):
        return False
    return True
