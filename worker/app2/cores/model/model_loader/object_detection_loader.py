from PIL import Image
from transformers import AutoImageProcessor, DeformableDetrForObjectDetection
import torch
id_use = [2,10,
11,
18,
22,
28,
33,
34,
 35,
 44,
 56,
 60,
 76,
 79,
 87,
 93,
 98,
 109,
 117,
 126,
 131,
 132,
 138,
 142,
 145,
 149,
 159,
 172,
 176,
 182,
 188,
 193,
 206,
 216,
 224,
 231,
 270,
 276,
 295,
 343,
 360,
 377,
 391,
 408,
 410,
 428,
 460,
 468,
 497,
 499,
 543,
 588,
 591,
 614,
 616,
 625,
 630,
 641,
 644,
 654,
 674,
 686,
 693,
 702,
 704,
 714,
 734,
 747,
 792,
 799,
 810,
 815,
 817,
 827,
 834,
 836,
 875,
 880,
 884,
 897,
 910,
 911,
 920,
 922,
 942,
 946,
 947,
 950,
 958,
 961,
 980,
 981,
 999,
 1007,
 1020,
 1025,
 1026,
 1034,
 1036,
 1041,
 1049,
 1070,
 1071,
 1077,
 1078,
 1096,
 1098,
 1101,
 1109,
 1111,
 1114,
 1116,
 1121,
 1122,
 1132,
 1140,
 1160,
 1161]
class ObjectDetection():
    def __init__(self):
        self.processor = AutoImageProcessor.from_pretrained("facebook/deformable-detr-box-supervised")
        self.model = DeformableDetrForObjectDetection.from_pretrained("facebook/deformable-detr-box-supervised")

    def predict(self, file_path):
        image = Image.open(file_path)
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.6)[0]
        output_dict = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            if label.item() not in id_use:
                continue
            box = [round(i, 2) for i in box.tolist()]
            output_dict.append({"box": str(list(box)), "class": int(label.item()), "score": str(round(score.item(), 3))})
        return output_dict
