import numpy as np

__all__ = ['get_image_blob']

def get_image_blob(image: np.ndarray, scalefactor: float, size: tuple[int, int], mean: tuple[float, float, float], swaprb: bool, crop: bool) -> np.ndarray: ...
