import os
import shutil
from typing import List, Optional
from imgutils.metrics import ccip_extract_feature, ccip_clustering
from PIL import Image


def load_images_from_folder(folder_path: str) -> List[Image.Image]:
    images = []
    file_paths = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # 尝试使用 Pillow 加载图像
            img = Image.open(file_path).convert('RGB')  # 确保将图像转换为 RGB 格式
            images.append(img)
            file_paths.append(file_path)
        except Exception as e:
            print(f"Error loading image {file_path}: {e}")
    return images, file_paths


def create_folder(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def copy_images_to_clusters(file_paths: List[str], cluster_ids: List[int], output_dir: str):
    # 创建输出目录
    create_folder(output_dir)

    # 创建每个簇的文件夹，并保存图像
    for file_path, cluster_id in zip(file_paths, cluster_ids):
        cluster_folder = os.path.join(output_dir, f'cluster_{cluster_id}')
        create_folder(cluster_folder)

        # 调试输出：显示文件路径和目标文件夹
        print(f"Copying {file_path} to {cluster_folder}")

        # 复制图像到对应的簇文件夹中
        shutil.copy(file_path, os.path.join(cluster_folder, os.path.basename(file_path)))


def cluster_and_save_images(folder_path: str, output_dir: str,
                            model: str = 'ccip-caformer-24-randaug-pruned',
                            eps: Optional[float] = None, min_samples: Optional[int] = None):
    # 读取文件夹中的所有图像
    images, file_paths = load_images_from_folder(folder_path)

    # 提取每个图像的特征
    features = [ccip_extract_feature(image, model=model) for image in images]

    # 聚类
    cluster_ids = ccip_clustering(features, method='optics_best', eps=None, min_samples=2, model=model)

    # 调试输出：显示聚类结果
    print("Cluster IDs:", cluster_ids)

    # 复制图像到对应的簇文件夹中
    copy_images_to_clusters(file_paths, cluster_ids, output_dir)


# 示例用法
if __name__ == "__main__":
    input_folder = 'img'
    output_folder = './img2'
    cluster_and_save_images(input_folder, output_folder)
