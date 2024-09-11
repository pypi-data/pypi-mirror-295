import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, ParseError

import PIL
import PIL.Image
from PIL.Image import Image

from ..errors import PascalParseError
from ..model import AAULabel, AAULabelImage, BoundingBox
from ..protocols import Label, LabelImage, LabelImageDeserializer, LabelImageSerializer


class Pascal(LabelImageDeserializer, LabelImageSerializer):
    file_extension = ".xml"

    def __init__(self, label_dir: Union[str, Path], indent: int = 4) -> None:
        self.label_dir = Path(label_dir) if isinstance(label_dir, str) else label_dir
        self.indent = indent

    def serialize(self, label_img: LabelImage) -> str:
        annotation = ET.Element("annotation")

        rel_img_path = os.path.relpath(label_img.path, self.label_dir)
        ET.SubElement(annotation, "folder").text = label_img.path.parent.name
        ET.SubElement(annotation, "filename").text = label_img.path.name
        ET.SubElement(annotation, "path").text = rel_img_path

        self.__add_source_element(annotation, label_img)
        self.__add_size_element(annotation, label_img)
        self.__add_segmented_element(annotation)
        self.__add_object_elements(annotation, label_img)

        return self.__prettify(annotation)

    def __deserialize(self, image_file: Path, label_file: Path, image: Image):
        try:
            root = ElementTree.parse(label_file).getroot()
            width, height = image.size
            labels = [
                self.__parse_object(child) for child in root if child.tag == "object"
            ]
            return AAULabelImage(image_file, width, height, labels)
        except ParseError as e:
            raise PascalParseError(label_file) from e

    def deserialize(
        self, image_file: Path, label_file: Path, image: Image | None = None
    ) -> LabelImage:
        if image is None:
            image = PIL.Image.open(image_file)
            return self.__deserialize(image_file, label_file, image)
        return self.__deserialize(image_file, label_file, image)

    def __prettify(self, elem: Element):
        """Return a pretty-printed XML string for the Element."""
        rough_string = ET.tostring(elem, "unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent=" " * self.indent)

    def __add_source_element(self, element: Element, label_img: LabelImage) -> None:
        source = ET.SubElement(element, "source")
        credit = "Unknown"
        ET.SubElement(source, "database").text = credit

    def __add_size_element(self, element: Element, label_img: LabelImage) -> None:
        size = ET.SubElement(element, "size")
        ET.SubElement(size, "width").text = str(label_img.width)
        ET.SubElement(size, "height").text = str(label_img.height)
        ET.SubElement(size, "depth").text = str(3)

    def __add_segmented_element(self, element: Element) -> None:
        ET.SubElement(element, "segmented").text = str(0)

    def __add_object_elements(self, element: Element, label_img: LabelImage) -> None:
        for label in label_img.labels:
            object_element = ET.SubElement(element, "object")
            ET.SubElement(object_element, "name").text = label.name
            ET.SubElement(object_element, "pose").text = "Unspecified"
            ET.SubElement(object_element, "truncated").text = str(0)
            ET.SubElement(object_element, "difficult").text = str(0)

            bndbox = ET.SubElement(object_element, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(label.x)
            ET.SubElement(bndbox, "ymin").text = str(label.y)
            ET.SubElement(bndbox, "xmax").text = str(label.x + label.width)
            ET.SubElement(bndbox, "ymax").text = str(label.y + label.height)

    def __parse_object(self, element: Element) -> Label:
        classifier: str
        bounding_box: BoundingBox

        for child in element:
            if child.tag == "name":
                classifier = child.text or ""
            elif child.tag == "bndbox":
                bounding_box = self.__parse_bounding_box(child)

        return AAULabel(
            bounding_box.xmin,
            bounding_box.ymin,
            bounding_box.xmax - bounding_box.xmin,
            bounding_box.ymax - bounding_box.ymin,
            classifier,
        )

    def __parse_bounding_box(self, element: Element):
        xmin: int
        ymin: int
        xmax: int
        ymax: int

        for child in element:
            if child.tag not in {"xmin", "ymin", "xmax", "ymax"}:
                continue
            if not child.text:
                raise ValueError(f"{child.tag} is missing")

            if child.tag == "xmin":
                xmin = int(child.text)
            elif child.tag == "ymin":
                ymin = int(child.text)
            elif child.tag == "xmax":
                xmax = int(child.text)
            elif child.tag == "ymax":
                ymax = int(child.text)

        return BoundingBox(xmin, ymin, xmax, ymax)
