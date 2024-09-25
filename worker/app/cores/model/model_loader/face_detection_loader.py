from deepface import DeepFace
class FaceDetection():
    def __init__(self):
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
            embedding_objs = DeepFace.represent(
                img_path = face['face'],
                enforce_detection = False,
                model_name  = 'GhostFaceNet'
                )
            for embedding_obj in embedding_objs:
                embedding = embedding_obj["embedding"]
                face_info['embedding'] = embedding
            data.append(face_info)

        return data

