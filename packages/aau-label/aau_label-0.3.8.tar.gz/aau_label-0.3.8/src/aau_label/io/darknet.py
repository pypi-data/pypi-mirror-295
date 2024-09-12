import logging
from pathlib import Path
from typing import Sequence

import PIL
import PIL.Image
from PIL.Image import Image

from ..errors import ClassFileNotFoundError, DarknetParseError
from ..model import AAULabel, AAULabelImage
from ..protocols import Label, LabelImage, LabelImageDeserializer, LabelImageSerializer


class Darknet(LabelImageDeserializer, LabelImageSerializer):
    file_extension = ".txt"

    def __init__(self, labels: Sequence[str]) -> None:
        self.__labels = labels
        self.__class_map = {label: i for i, label in enumerate(labels)}
        self.__logger = logging.getLogger(__class__.__name__)

    @staticmethod
    def load_class_file(class_file: Path) -> Sequence[str]:
        try:
            with open(class_file, "r") as file:
                return [row.strip() for row in file if row]
        except FileNotFoundError as e:
            raise ClassFileNotFoundError(class_file) from e

    def serialize(self, label_img: LabelImage) -> str:
        rv = ""

        for label in label_img.labels:
            class_id = self.__class_map.get(label.name)
            if class_id is None:
                self.__logger.warning(f"{label.name} not in provided class map")
                continue

            x = (label.x + label.width / 2) / label_img.width
            y = (label.y + label.height / 2) / label_img.height
            width = label.width / label_img.width
            height = label.height / label_img.height
            rv += f"{class_id} {x} {y} {width} {height}\n"

        return rv

    def __deserialize(self, image_file: Path, label_file: Path, image: Image):
        with open(label_file, "r") as file:
            width, height = image.size
            try:
                labels = [self.__parse_row(row, width, height) for row in file]
                return AAULabelImage(image_file, width, height, labels)
            except ValueError:
                raise DarknetParseError(label_file)

    def deserialize(
        self, image_file: Path, label_file: Path, image: Image | None = None
    ) -> LabelImage:
        if image is None:
            with PIL.Image.open(image_file) as image:
                return self.__deserialize(image_file, label_file, image)
        return self.__deserialize(image_file, label_file, image)

    def __parse_row(self, row: str, img_width, img_height) -> Label:
        class_index, x, y, width, height = row.split()

        class_index = int(class_index)
        width = round(float(width) * img_width)
        height = round(float(height) * img_height)
        x = round(float(x) * img_width - width / 2)
        y = round(float(y) * img_height - height / 2)

        return AAULabel(x, y, width, height, self.__labels[class_index])
