from typing import Any

from .protocols import LabelImage


def label_image_to_dict(label_image: LabelImage) -> dict[str, Any]:
    return {
        "path": label_image.path.as_posix(),
        "width": label_image.width,
        "height": label_image.height,
        "labels": [
            {
                "x": label.x,
                "y": label.y,
                "width": label.width,
                "height": label.height,
                "name": label.name,
            }
            for label in label_image.labels
        ],
    }
