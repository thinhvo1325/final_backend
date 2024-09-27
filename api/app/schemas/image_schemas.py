from pydantic import BaseModel
from typing import Optional
from cores.common import dump_str_to_date_format
from typing import Any

object_name_id = {
    'người': 1,
    'xe đạp': 2,
    'xe ô tô': 3,
    'xe máy': 4,
    'máy bay': 5,
    'xe buýt': 6,
    'tàu hỏa': 7,
    'xe tải': 8,
    'thuyền': 9,
    'đèn giao thông': 10,
    'vòi nước cứu hỏa': 11,
    'biển báo dừng': 12,
    'đồng hồ tính tiền đậu xe': 13,
    'ghế băng': 14,
    'chim': 15,
    'mèo': 16,
    'chó': 17,
    'ngựa': 18,
    'cừu': 19,
    'bò': 20,
    'voi': 21,
    'gấu': 22,
    'ngựa vằn': 23,
    'hươu cao cổ': 24,
    'ba lô': 25,
    'ô (dù)': 26,
    'túi xách tay': 27,
    'cà vạt': 28,
    'vali': 29,
    'đĩa ném': 30,
    'ván trượt tuyết': 32,
    'quả bóng thể thao': 33,
    'diều': 34,
    'gậy bóng chày': 35,
    'găng tay bóng chày': 36,
    'ván trượt': 37,
    'ván lướt sóng': 38,
    'vợt tennis': 39,
    'chai': 40,
    'ly rượu vang': 41,
    'tách': 42,
    'nĩa': 43,
    'dao': 44,
    'muỗng': 45,
    'bát': 46,
    'chuối': 47,
    'táo': 48,
    'bánh sandwich': 49,
    'cam': 50,
    'bông cải xanh': 51,
    'cà rốt': 52,
    'xúc xích kẹp bánh mì': 53,
    'bánh pizza': 54,
    'bánh rán': 55,
    'bánh ngọt': 56,
    'ghế': 57,
    'ghế sofa': 58,
    'cây trồng trong chậu': 59,
    'giường': 60,
    'bàn ăn': 61,
    'nhà vệ sinh': 62,
    'tivi': 63,
    'máy tính xách tay': 64,
    'chuột': 65,
    'điều khiển từ xa': 66,
    'bàn phím': 67,
    'điện thoại di động': 68,
    'lò vi sóng': 69,
    'lò nướng': 70,
    'máy nướng bánh mì': 71,
    'bồn rửa': 72,
    'tủ lạnh': 73,
    'sách': 74,
    'đồng hồ': 75,
    'lọ hoa': 76,
    'kéo': 77,
    'gấu bông': 78,
    'máy sấy tóc': 79,
    'bàn chải đánh răng': 80,
    'văn bản': 81
}

class ImageFileSearchSchema(BaseModel):
    image_id: Optional[str] = None
    created_date: Optional[str] = None
    status: Optional[int] = None
    user_id: Optional[int] = None
    is_public: Optional[bool] = None
    text: Optional[str] = None
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
