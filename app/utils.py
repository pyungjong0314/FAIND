from torchreid.utils import FeatureExtractor
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 전역으로 Re-ID feature extractor 생성
extractor = FeatureExtractor(
    model_name='osnet_x1_0',
    model_path='',  # 사전학습된 모델 자동 다운로드
    device='cpu'    # or 'cuda'
)

def extract_feature_vector(image: np.ndarray) -> np.ndarray:
    # 이미지 파일 경로를 받아 Re-ID feature vector (numpy array)를 반환한다.
    
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    features = extractor([rgb_image])
    return features[0]

def compute_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    # 두 feature vector 간의 코사인 유사도를 계산해 반환한다.
    
    return float(cosine_similarity([vec1], [vec2])[0][0])


def apply_mosaic_to_head(image, xmin, ymin, xmax, ymax, mosaic_ratio=0.1):
    head_height = int((ymax - ymin) * 0.3)
    head_ymax = ymin + head_height
    head_region = image[ymin:head_ymax, xmin:xmax]

    if head_region.size == 0:
        return image

    small = cv2.resize(head_region, (max(1, int((xmax - xmin) * mosaic_ratio)), max(1, int(head_height * mosaic_ratio))), interpolation=cv2.INTER_LINEAR)
    mosaic = cv2.resize(small, (xmax - xmin, head_height), interpolation=cv2.INTER_NEAREST)

    image[ymin:head_ymax, xmin:xmax] = mosaic
    return image
