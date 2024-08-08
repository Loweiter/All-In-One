import logging
import os
import pickle
import time

import clip
import torch
from PIL import Image

# 配置日志记录
logging.basicConfig(level=logging.INFO)

def extract_features(img_paths, model, preprocess, device, batch_size=32):
    all_features = []
    for i in range(0, len(img_paths), batch_size):
        batch_paths = img_paths[i:i+batch_size]
        images = [preprocess(Image.open(p)).unsqueeze(0).to(device) for p in batch_paths]
        images = torch.cat(images)
        with torch.no_grad():
            features = model.encode_image(images)
        all_features.extend(features.cpu().numpy())
    return all_features

def cache_features(directory, model, preprocess, device, cache_file="features_cache.pkl"):
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)
    img_paths = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith("webp"):
                img_path = os.path.join(root, filename)
                img_paths.append(img_path)
    features_list = extract_features(img_paths, model, preprocess, device)
    features_dict = dict(zip(img_paths, features_list))
    with open(cache_file, "wb") as f:
        pickle.dump(features_dict, f)
    return features_dict

# 指定目录
directory = "/Users/zhouhongxiang/PycharmProjects/pythonProject"

# 统计缓存特征时间
start_time = time.time()
# 加载CLIP模型
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
features_dict = cache_features(directory, model, preprocess, device)
end_time = time.time()
logging.info(f"Caching features took {end_time - start_time:.2f} seconds")

# 比较两张图片的相似度
def cosine_similarity_pytorch(x, y):
    x = torch.tensor(x)
    y = torch.tensor(y)
    return torch.nn.functional.cosine_similarity(x, y.unsqueeze(0)).item()

def find_most_similar(target_img_paths, features_dict, model, preprocess, device):
    results = {}
    target_features_list = extract_features(target_img_paths, model, preprocess, device)
    for target_img_path, target_features in zip(target_img_paths, target_features_list):
        similarities = {}
        for img_path, features in features_dict.items():
            similarity = cosine_similarity_pytorch(target_features, features)
            similarities[img_path] = similarity
        most_similar_path = max(similarities, key=similarities.get)
        results[target_img_path] = (most_similar_path, similarities[most_similar_path])
    return results

# 遍历文件夹中的所有图片作为目标图片
target_directory = "/Users/zhouhongxiang/PycharmProjects/pythonProject/img"
target_img_paths = []
for root, _, files in os.walk(target_directory):
    for filename in files:
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith("webp"):
            img_path = os.path.join(root, filename)
            target_img_paths.append(img_path)

# 统计查找相似图片时间
start_time = time.time()
similarity_results = find_most_similar(target_img_paths, features_dict, model, preprocess, device)
end_time = time.time()
logging.info(f"Finding similar images took {end_time - start_time:.2f} seconds")

for target_img_path, (most_similar_path, similarity_score) in similarity_results.items():
    logging.info(f"Target image: {target_img_path}")
    logging.info(f"Most similar image: {most_similar_path} with similarity score: {similarity_score}")
