from pydantic import BaseModel
from typing import Optional
from cores.common import dump_str_to_date_format
from typing import Any

object_name_id ={
    'máy bay': 2,
    'ăng-ten': 10,
    'táo': 11,
    'ghế bành': 18,
    'thùng rác': 22,
    'mái hiên': 28,
    'ba lô': 33,
    'túi xách': 34,
    'vali': 35,
    'chuối': 44,
    'bóng chày': 56,
    'giỏ': 60,
    'giường': 76,
    'bò': 79,
    'thắt lưng': 87,
    'xe đạp': 93,
    'chim': 98,
    'chăn': 109,
    'thuyền': 117,
    'sách': 126,
    'giày ủng': 131,
    'chai': 132,
    'bát': 138,
    'hộp': 142,
    'vòng tay': 145,
    'bánh mì': 149,
    'xô': 159,
    'xe buýt': 172,
    'nút bấm': 176,
    'bánh kem': 182,
    'máy ảnh': 188,
    'nến': 193,
    'xe hơi': 206,
    'cà rốt': 216,
    'mèo': 224,
    'ghế': 231,
    'đồng hồ': 270,
    'áo khoác': 276,
    'bàn phím máy tính': 295,
    'cốc': 343,
    'bàn': 360,
    'chó': 377,
    'váy': 391,
    'tai nghe': 408,
    'bông tai': 410,
    'quạt': 428,
    'bình hoa': 460,
    'nĩa': 468,
    'ly': 497,
    'găng tay': 499,
    'mũ': 543,
    'áo khoác': 588,
    'quần jean': 591,
    'dao': 614,
    'núm': 616,
    'đèn': 625,
    'máy tính xách tay': 630,
    'biển số xe': 641,
    'bóng đèn': 644,
    'loa': 654,
    'mặt nạ': 674,
    'lò vi sóng': 686,
    'gương': 693,
    'xe máy': 702,
    'chuột máy tính': 704,
    'vòng cổ': 714,
    'cam': 734,
    'tranh': 747,
    'người': 792,
    'xe bán tải': 799,
    'ống': 810,
    'bánh pizza': 815,
    'đĩa': 817,
    'áo polo': 827,
    'áp phích': 834,
    'chậu cây': 836,
    'gương chiếu hậu': 875,
    'điều khiển từ xa': 880,
    'nhẫn': 884,
    'túi nhựa': 897,
    'dép xăng đan': 910,
    'bánh sandwich': 911,
    'khăn quàng cổ': 920,
    'kéo': 922,
    'cừu': 942,
    'áo sơ mi': 946,
    'giày': 947,
    'quần đùi': 950,
    'biển báo': 958,
    'ván trượt': 961,
    'tất': 980,
    'ghế sofa': 981,
    'thìa': 999,
    'tượng': 1007,
    'bếp': 1020,
    'biển báo đường': 1025,
    'đèn đường': 1026,
    'kính râm': 1034,
    'ván lướt sóng': 1036,
    'áo len': 1041,
    'bàn': 1049,
    'gấu bông': 1070,
    'điện thoại': 1071,
    'bóng tennis': 1077,
    'vợt tennis': 1078,
    'nhà vệ sinh': 1096,
    'cà chua': 1098,
    'bàn chải đánh răng': 1101,
    'đồ chơi': 1109,
    'đèn giao thông': 1111,
    'tàu hỏa': 1114,
    'khay': 1116,
    'quần dài': 1121,
    'xe tải': 1122,
    'ô': 1132,
    'lỗ thông gió': 1140,
    'đồng hồ đeo tay': 1160,
    'chai nước': 1161
}


class ImageFileSearchSchema(BaseModel):
    image_id: Optional[str] = None
    created_date: Optional[str] = None
    status: Optional[int] = None
    user_id: Optional[int] = None
    is_public: Optional[bool] = None
    text: Optional[str] = None
    face: Optional[str] = None
    object_name: Optional[str] = None

    def model_dump(self, **kwargs) -> dict[str, Any]:
        change_names = {
             'text': 'text_list','object_name': 'object_id',
            'collection_id': 'collection', 'storage_id': 'storage'
        }
        data = super(ImageFileSearchSchema, self).model_dump(**kwargs)
        return_data = {}
        for key, value in data.items():
            if value is not None:
                if key in change_names.keys():
                    return_data.update({change_names.get(key): value})
                else:
                    return_data.update({key: value})
        return_data_new = {}
        for key, value in return_data.items():
            if value is not None:
                if key in ["created_date"]:
                    return_data_new.update({key: dump_str_to_date_format(value)})
                elif key in ["object_id"]:
                    return_data_new.update({key: object_name_id[value]})
                else:
                    return_data_new.update({key: value})
        return return_data_new
    

class ImageUpdateSchema(BaseModel):
    image_id: Optional[list[str]] = None
    status: Optional[int] = None
    is_public: Optional[bool] = None
