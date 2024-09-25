import keras_ocr
class TextDetection():
    def __init__(self):
        self.predicter = keras_ocr.pipeline.Pipeline()
        
    def predict(self, file_path):
        result = self.predicter.recognize([file_path])
        return result[0]

