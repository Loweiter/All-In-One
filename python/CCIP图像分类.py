import os
import shutil
from typing import List, Optional
from imgutils.metrics import ccip_extract_feature, ccip_clustering
from PIL import Image

"""
对给定的图像或特征向量列表进行聚类。

该函数应用选定的聚类方法（method）和指定的参数（eps 和 min_samples）来对提供的图像或特征向量（images）进行聚类。

默认的 eps 和 min_samples 值是通过 :func:`ccip_default_clustering_params` 函数基于选定的方法（method）和模型（model）获得的。如果未提供 eps 和 min_samples 的值，将使用默认值。

图像或特征向量会根据指定的 size 和 model 参数进行预处理并转换为特征表示。特征向量之间的成对差异是通过 :func:`ccip_batch_differences` 函数计算的，以定义聚类的距离度量。

聚类是使用 DBSCAN 算法或 OPTICS 算法执行的，具体取决于选定的方法（method）。聚类标签作为 NumPy 数组返回。

参数:
- images: 要聚类的图像或特征向量列表。
  类型: List[_FeatureOrImage]

- method: 聚类方法，用于获取默认参数。（默认: `optics`）
  可用选项: `dbscan`, `dbscan_2`, `dbscan_free`, `optics`, `optics_best`。
  类型: CCIPClusterMethodTyping

- eps: 两个样本之间被视为同一邻域的最大距离。（默认: `None`）
  如果为 None，则使用 :func:`ccip_default_clustering_params` 获得的默认值。
  类型: Optional[float]

- min_samples: 一个点被视为核心点的邻域中的最小样本数。（默认: `None`）
  如果为 None，则使用 :func:`ccip_default_clustering_params` 获得的默认值。
  类型: Optional[int]

- size: 用于特征提取的图像大小。（默认: `384`）
  类型: int

- model: 用于特征提取的模型名称。（默认: `ccip-caformer-24-randaug-pruned`）
  可用模型名称: `ccip-caformer-24-randaug-pruned`, `ccip-caformer-6-randaug-pruned_fp32`, `ccip-caformer-5_fp32`。
  类型: str

返回:
- 一个表示每个图像或特征向量的聚类分配的标签数组。
  类型: np.ndarray

示例:
以下是所有图像

.. image:: ccip_full.plot.py.svg
    :align: center

>>> from imgutils.metrics import ccip_clustering
>>>
>>> images = [f'ccip/{i}.jpg' for i in range(1, 13)]
>>> images
['ccip/1.jpg', 'ccip/2.jpg', 'ccip/3.jpg', 'ccip/4.jpg', 'ccip/5.jpg', 'ccip/6.jpg', 'ccip/7.jpg', 'ccip/8.jpg', 'ccip/9.jpg', 'ccip/10.jpg', 'ccip/11.jpg', 'ccip/12.jpg']
>>>
>>> # 图像数量较少时，min_samples 不应设置过大
>>> ccip_clustering(images, min_samples=2)
[0, 0, 0, 3, 3, 3, 1, 1, 1, 1, 2, 2]

注意:
请注意，CCIP 中的聚类过程对参数非常敏感，可能需要调整。因此，建议遵循以下指南：

1. 处理大量样本时，建议使用 `optics` 方法的默认参数进行聚类。这有助于确保聚类解决方案的鲁棒性。

2. 如果样本数量较少，建议在执行聚类之前减少 `min_samples` 参数的值。然而需要注意的是，这可能会显著增加将同一角色的稍微不同实例分离到不同簇中的可能性。

3. 在样本整体上表现出规律性模式的情况下（例如具有清晰特征和一致姿势和服装的角色），可以考虑使用 `dbscan` 方法进行聚类。然而请注意，dbscan 方法对 `eps` 值非常敏感，因此需要仔细调整。
 """

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
    # 特征标准化
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # 聚类
    cluster_ids = ccip_clustering(features_scaled, method='optics_best', eps=None, min_samples=2, model=model)

    # 调试输出：显示聚类结果
    print("Cluster IDs:", cluster_ids)

    # 复制图像到对应的簇文件夹中
    copy_images_to_clusters(file_paths, cluster_ids, output_dir)


# 示例用法
if __name__ == "__main__":
    input_folder = 'img'
    output_folder = './img2'
    cluster_and_save_images(input_folder, output_folder)
