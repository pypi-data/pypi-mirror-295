import dataclasses
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from pandas import DataFrame

from . import utilities
from .errors import LabelError
from .io import Darknet, Pascal
from .model import AAULabel, AAULabelImage, COCOInfo, COCOLicense
from .protocols import Label, LabelImage, LabelImageDeserializer

logger = logging.getLogger(__name__)


def from_file(filepath: str | Path) -> list[LabelImage]:
    label_images = []
    with open(filepath, "r") as file:
        data = json.load(file)

        for element in data:
            labels: list[Label] = []
            for label_dict in element["labels"]:
                label = AAULabel(
                    label_dict["x"],
                    label_dict["y"],
                    label_dict["width"],
                    label_dict["height"],
                    label_dict["classifier"],
                )
                labels.append(label)

            label_image = AAULabelImage(
                path=element["path"],
                width=element["width"],
                height=element["height"],
                labels=labels,
            )
            label_images.append(label_image)

    return label_images


def __get_files_with_extensions(
    directory: Path, extensions: set[str]
) -> Iterable[Path]:
    for file in directory.iterdir():
        if file.suffix.lower() in extensions:
            yield file


def __join_label_and_image_files(
    images: Iterable[Path], labels: Iterable[Path]
) -> Iterable[tuple[Path, Path]]:
    lookup = {path.stem: path for path in images}
    for label_path in labels:
        img_path = lookup.get(label_path.stem)
        if img_path is None:
            continue
        yield (img_path, label_path)


def from_dir(
    img_dir: str | Path,
    label_dir: str | Path,
    deserializer: LabelImageDeserializer,
) -> Iterable[LabelImage]:
    if isinstance(img_dir, str):
        img_dir = Path(img_dir)
    if isinstance(label_dir, str):
        label_dir = Path(label_dir)

    if not img_dir.exists() or not label_dir.exists():
        return

    image_paths = __get_files_with_extensions(img_dir, {".jpg", ".jpeg", ".png"})
    label_paths = __get_files_with_extensions(label_dir, {deserializer.file_extension})
    pairs = __join_label_and_image_files(image_paths, label_paths)

    for img_path, label_path in pairs:
        try:
            yield deserializer.deserialize(img_path, label_path)
        except (FileNotFoundError, ValueError, LabelError) as error:
            logger.warning(error)


def from_pascal_dir(img_dir: str | Path, label_dir: str | Path) -> Iterable[LabelImage]:
    return from_dir(img_dir, label_dir, Pascal(label_dir))


def from_darknet_dir(
    img_dir: str | Path, label_dir: str | Path
) -> Iterable[LabelImage]:
    if isinstance(label_dir, str):
        label_dir = Path(label_dir)

    class_file = label_dir.joinpath("classes.txt")
    classes = Darknet.load_class_file(class_file)
    return from_dir(img_dir, label_dir, Darknet(classes))


def write(filepath: str | Path, label_images: Iterable[LabelImage]) -> None:
    label_image_dicts = map(utilities.label_image_to_dict, label_images)
    with open(filepath, "w") as file:
        json.dump(list(label_image_dicts), file, indent=2)


def __get_unique_classifiers(label_images: Iterable[LabelImage]) -> dict[str, int]:
    classifiers = set()
    for label_image in label_images:
        classifiers.update(label.name for label in label_image.labels)
    return {classifier: i for i, classifier in enumerate(classifiers)}


def to_coco(
    label_images: Iterable[LabelImage], license: COCOLicense, info: COCOInfo
) -> dict[str, Any]:
    logger.info("Extracting unique labels from LabelImage objects")
    classifier_db = __get_unique_classifiers(label_images)

    categories = [
        {"id": id, "name": name, "supercategory": ""}
        for name, id in classifier_db.items()
    ]

    images = []
    annotations = []

    label_id = 0
    for image_id, label_image in enumerate(label_images):
        images.append(
            {
                "id": image_id,
                "width": label_image.width,
                "height": label_image.height,
                "file_name": Path(label_image.path).name,
                "license": 0,
                "flickr_url": "",
                "coco_url": label_image.path,
                "date_captured": datetime.now(),
            }
        )
        for label in label_image.labels:
            annotations.append(
                {
                    "id": label_id,
                    "image_id": image_id,
                    "category_id": classifier_db[label.name],
                    "bbox": [label.x, label.y, label.width, label.height],
                    "iscrowd": 0,
                }
            )
            label_id += 1

    return {
        "info": dataclasses.asdict(info),
        "images": images,
        "annotations": annotations,
        "categories": categories,
        "licenses": [
            {
                "id": 0,
                "name": license.name,
                "url": license.url,
            }
        ],
    }


def to_dataframe(label_images: Sequence[LabelImage]) -> DataFrame:
    rows = []
    for label_image in label_images:
        rows.extend(
            {
                "path": label_image.path,
                "image_width": label_image.width,
                "image_height": label_image.height,
                "label_width": label.width,
                "label_height": label.height,
                "x": label.x,
                "y": label.y,
                "classifier": label.name,
            }
            for label in label_image.labels
        )
    return DataFrame(rows)


def from_dataframe(df: DataFrame) -> Iterable[LabelImage]:
    group_by = df.groupby(["path", "image_width", "image_height"])
    for (path, width, height), group in group_by:  # type: ignore
        labels: Sequence[Label] = [
            AAULabel(
                label["x"],  # type: ignore
                label["y"],  # type: ignore
                label["label_width"],  # type: ignore
                label["label_height"],  # type: ignore
                label["classifier"],  # type: ignore
            )
            for _, label in group.iterrows()
        ]

        yield AAULabelImage(path, width, height, labels)  # type: ignore
