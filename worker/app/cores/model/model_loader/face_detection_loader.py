from deepface import DeepFace
import cv2 
# See github.com/timesler/facenet-pytorch:
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face
import torch
from PIL import Image
from torchvision.transforms import ToTensor
class FaceDetection():
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.resnet = InceptionResnetV1(pretrained='vggface2', device=self.device).eval()
        pass
    def predict(self, file_path):
        face_objs = DeepFace.extract_faces(
            img_path = file_path, 
            detector_backend = 'fastmtcnn',
            align = True,
            enforce_detection = False,
        )
        data = []
        for face in face_objs:
            face_info = {}
            face_info['facial_area'] = face['facial_area']

            image = cv2.imread(file_path)
            x, y, w, h = face['facial_area']['x'], face['facial_area']['y'], face['facial_area']['w'], face['facial_area']['h']
            face_image = image[y:y+h, x:x+w]
            # Save the cropped face image
            cv2.imwrite(file_path+'.jpg', face_image)
            tf_img = lambda i: ToTensor()(i).unsqueeze(0)
            embeddings = lambda input: self.resnet(input)
            t = tf_img(Image.open(file_path+'.jpg')).to(self.device)
            e = embeddings(t).squeeze().cpu().tolist()
            face_info['embedding'] = e
            face_info['cluster'] = -5
            data.append(face_info)

        return data

