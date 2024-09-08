# akaOCR

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.7](https://img.shields.io/badge/python-3.7+-aff.svg)](https://www.python.org/downloads/release/python-370/)
[![ONNX Compatible](https://img.shields.io/badge/ONNX-Compatible-brightgreen)](https://onnx.ai/)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.google/)


## Description

This package is compatible with [akaOCR](https://app.akaocr.io/) for ocr pipeline program (Text Detection, Text Recognition & Text Rotation), using [ONNX](https://onnx.ai/) format model (CPU & GPU speed can be **x2 Times Faster**). This code is referenced from [this awesome repo](https://github.com/PaddlePaddle/PaddleOCR).

## Features

Feature 1: **Text Detection**.

```python
from akaocr import BoxEngine
import cv2

img_path = "path/to/image.jpg"
image = cv2.imread(img_path)

# side_len: minimum inference image size
box_engine = BoxEngine(model_path: Any | None = None,
                        side_len: int | None = None,
                        conf_thres: float = 0.5
                        mask_thes: float = 0.4,
                        unclip_ratio: float = 2.0,
                        max_candidates: int = 1000,
                        device: str = 'cpu | gpu')

# inference for one image
results = box_engine(image) # [np.array([4 points], dtype=np.float32),...]
```

Feature 2: **Text Recognition**.

```python
from akaocr import TextEngine
import cv2

img_path = "path/to/cropped_image.jpg"
cropped_image = cv2.imread(img_path)

text_engine = TextEngine(model_path: Any | None = None,
                        vocab_path: Any | None = None,
                        use_space_char: bool = True,
                        batch_sizes: int = 32,
                        model_shape: list = [3, 48, 320],
                        max_wh_ratio: int = None,
                        device: str = 'cpu | gpu')

# inference for one or more images
results = text_engine(cropped_image) # [(text, conf),...]
```

Feature 3: **Text Rotation**.

```python
from akaocr import ClsEngine
import cv2

img_path = "path/to/cropped_image.jpg"
cropped_image = cv2.imread(img_path)

rotate_engine = ClsEngine(model_path: Any | None = None,
                        conf_thres: float = 0.75
                        device: str='cpu | gpu')

# classify input image as 0 or 180 degrees
# inference for one or more images
results = rotate_engine(cropped_image) # [(lable (0|180), conf),...]
```

## Usage

1. **Perspective Transform Image**.

```python
import numpy as np

def transform_image(image, box):
    # Get perspective transform image

    assert len(box) == 4, "Shape of points must be 4x2"
    img_crop_width = int(
        max(
            np.linalg.norm(box[0] - box[1]),
            np.linalg.norm(box[2] - box[3])))
    img_crop_height = int(
        max(
            np.linalg.norm(box[0] - box[3]),
            np.linalg.norm(box[1] - box[2])))
    pts_std = np.float32([[0, 0], 
                        [img_crop_width, 0],
                        [img_crop_width, img_crop_height],
                        [0, img_crop_height]])
    M = cv2.getPerspectiveTransform(box, pts_std)
    dst_img = cv2.warpPerspective(
        image,
        M, (img_crop_width, img_crop_height),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC)
    
    img_height, img_width = dst_img.shape[0:2]
    if img_height/img_width >= 1.5:
            dst_img = np.rot90(dst_img, k=3)

    return dst_img
```

2. **OCR Pipeline**.

```python
from akaocr import TextEngine
from akaocr import BoxEngine

import cv2

box_engine = BoxEngine()
text_engine = TextEngine()

def main():
    img_path = "sample.png"
    org_image = cv2.imread(img_path)
    images = []

    boxes = box_engine(org_image)
    for box in boxes:
        # crop & transform image
        image = transform_image(org_image, box)
        images.append(image)

    texts = text_engine(images)

if __name__ == '__main__':
    main()
```

**Note**: akaOCR (Transform documents into useful data with AI-based IDP - Intelligent Document Processing) - helps make inefficient manual entry a thing of the past—and reliable data insights a thing of the present. Details at: https://app.akaocr.io