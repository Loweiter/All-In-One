import logging
from functools import lru_cache

from PIL import Image
from imgutils.metrics import ccip_extract_feature, ccip_same

# 配置日志记录
logging.basicConfig(level=logging.INFO)

class ImageItem:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.meta = {}

@lru_cache(maxsize=128)
def extract_feature(image_path, model='ccip-caformer-24-randaug-pruned'):
    # 提取图像特征并缓存
    try:
        image = Image.open(image_path)
        feature = ccip_extract_feature(image, model=model)
        return feature
    except Exception as e:
        logging.error(f"Failed to extract feature from image {image_path}: {e}")
        return None

def compare_images(image_path1, image_path2, model='ccip-caformer-24-randaug-pruned'):
    # 提取特征
    feature1 = extract_feature(image_path1, model=model)
    feature2 = extract_feature(image_path2, model=model)
    if feature1 is None or feature2 is None:
        return None
    # 计算差异
    # differences = ccip_batch_differences([feature1, feature2], model=model)
    same = ccip_same(feature1, feature2 , model=model)
    return same

# 示例图片路径
image_path1 = '/Users/zhouhongxiang/PycharmProjects/pythonProject/img/u=771727465,3335130314&fm=253&app=120&size=w931&n=0&f=JPEG&fmt=auto.webp'
image_path2 = '/Users/zhouhongxiang/PycharmProjects/pythonProject/img/u=2927007463,4025565651&fm=253&app=120&size=w931&n=0&f=JPEG&fmt=auto.webp'

same = compare_images(image_path1, image_path2)
print(same)