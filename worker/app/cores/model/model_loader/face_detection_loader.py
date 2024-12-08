from deepface import DeepFace
import cv2 
# See github.com/timesler/facenet-pytorch:
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face
import torch
from PIL import Image
from torchvision.transforms import ToTensor
from mtcnn import MTCNN
from PIL import Image
import numpy as np
class FaceDetection():
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.resnet = InceptionResnetV1(pretrained='vggface2', device=self.device).eval()
        self.mtcnn_model = MTCNN()
        pass
    def predict(self, file_path):
        img = Image.open(file_path)
        image = img.convert('RGB')
        pixels = np.asarray(image)
        results = self.mtcnn_model.detect_faces(pixels)
        data = []
        for res in results:
            face_info = {}
            face_info['facial_area'] = res['box']
            x1, y1, width, height = res['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height

            face = pixels[y1:y2, x1:x2]
            image = Image.fromarray(face)
        
            image.save(file_path+'.jpg')
            tf_img = lambda i: ToTensor()(i).unsqueeze(0)
            embeddings = lambda input: self.resnet(input)
            t = tf_img(Image.open(file_path+'.jpg')).to(self.device)
            e = embeddings(t).squeeze().cpu().tolist()
            face_info['embedding'] = e
            face_info['cluster'] = -5
            data.append(face_info)

        return data

