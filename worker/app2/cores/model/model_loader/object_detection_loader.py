import tensorflow as tf
import numpy as np
from six import BytesIO
from PIL import Image
tf.keras.backend.clear_session()
class ObjectDetection():
    def __init__(self):
        self.predicter = tf.saved_model.load("cores/model/model/saved_model")
        
    def predict(self, file_path):
        # result = self.predicter.recognize([file_path])
        # return result[0]
        image_np = self.load_image_into_numpy_array(file_path)
        output_dict = self.run_inference_for_single_image(image_np)
        return output_dict
    
    def run_inference_for_single_image(self, image):
  
        image = np.asarray(image)
        input_tensor = tf.convert_to_tensor(image)
        input_tensor = input_tensor[tf.newaxis,...]

        model_fn = self.predicter.signatures['serving_default']
        output_dict = model_fn(input_tensor)

        num_detections = int(output_dict.pop('num_detections'))
        output_dict = {key:value[0, :num_detections].numpy() 
                    for key,value in output_dict.items()}
        output_dict['num_detections'] = num_detections
        output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
        return output_dict

    def load_image_into_numpy_array(self, path):
        img_data = tf.io.gfile.GFile(path, 'rb').read()
        image = Image.open(BytesIO(img_data))
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)
