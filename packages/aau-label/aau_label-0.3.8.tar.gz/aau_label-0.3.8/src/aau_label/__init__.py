import dataclasses
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence, cast

from pandas import DataFrame

from aau_label.errors import ClassFileNotFoundError

from . import utilities
from .io import Darknet, Pascal
from .model import AAULabel, AAULabelImage, COCOInfo, COCOLicense
from .protocols import Label, LabelImage, LabelImageDeserializer

logger = logging.getLogger(__name__)


class DeserializedLabelImageIterator(Iterator[LabelImage]):
    def __init__(
        self,
        img_label_pairs: Iterator[tuple[Path, Path]],
        deserializer: LabelImageDeserializer,
    ) -> None:
        self.__pairs = img_label_pairs
        self.__deserializer = deserializer

    def __iter__(self):
        return self

    def __next__(self) -> LabelImage:
        img_path, label_path = next(self.__pairs)
        return self.__deserializer.deserialize(img_path, label_path)


def from_file(filepath: str | Path) -> list[LabelImage]:
    """
    Loads a list of LabelImage objects from a AAU JSON file.

    Args:
        filepath (str | Path): The path to the AAU JSON file to load from.

    Returns:
        list[LabelImage]: A list of LabelImage objects loaded from the file.
    """
    label_images = []
    with open(filepath, "r") as file:
        data: list[dict[str, Any]] = json.load(file)

        for element in data:
            labels: list[Label] = []
            for label_dict in element["labels"]:
                label_dict = cast(dict[str, Any], label_dict)
                # Old format uses classifier, new format uses name
                label_name = label_dict.get("classifier", label_dict["name"])

                label = AAULabel(
                    label_dict["x"],
                    label_dict["y"],
                    label_dict["width"],
                    label_dict["height"],
                    label_name,
                )
                labels.append(label)

            label_image = AAULabelImage(
                path=Path(element["path"]),
                width=element["width"],
                height=element["height"],
                labels=labels,
            )
            label_images.append(label_image)

    return label_images


def __get_files_with_extensions(
    directory: Path, extensions: set[str]
) -> Iterator[Path]:
    for file in directory.iterdir():
        if file.suffix.lower() in extensions:
            yield file


def __join_label_and_image_files(
    images: Iterable[Path], labels: Iterable[Path]
) -> Iterator[tuple[Path, Path]]:
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
) -> Iterator[LabelImage]:
    """
    Generate an iterator of LabelImage objects from a directory containing images and labels.

    Args:
        img_dir: The directory containing the images.
        label_dir: The directory containing the labels.
        deserializer: A LabelImageDeserializer instance used to deserialize the label files.

    Returns:
        Iterator[LabelImage]: Iterator over LabelImage instances.
    """
    if isinstance(img_dir, str):
        img_dir = Path(img_dir)
    if isinstance(label_dir, str):
        label_dir = Path(label_dir)

    if not img_dir.exists() or not label_dir.exists():
        return DeserializedLabelImageIterator(iter([]), deserializer)

    image_paths = __get_files_with_extensions(img_dir, {".jpg", ".jpeg", ".png"})
    label_paths = __get_files_with_extensions(label_dir, {deserializer.file_extension})
    pairs = __join_label_and_image_files(image_paths, label_paths)

    return DeserializedLabelImageIterator(pairs, deserializer)


def from_pascal_dir(img_dir: str | Path, label_dir: str | Path) -> Iterator[LabelImage]:
    """
    Generate an iterator of LabelImage objects from a directory containing images and labels in Pascal VOC format.

    Args:
        img_dir: The directory containing the images.
        label_dir: The directory containing the labels.

    Returns:
        Iterator[LabelImage]: Iterator over LabelImage instances.
    """
    return from_dir(img_dir, label_dir, Pascal(label_dir))


def from_darknet_dir(
    img_dir: str | Path,
    label_dir: str | Path,
    class_file: str | Path | None = None,
    strict: bool = False,
) -> Iterator[LabelImage]:
    """
    Load Darknet format labels and images from directories.

    Args:
        img_dir (str | Path): Directory containing image files.
        label_dir (str | Path): Directory containing Darknet format label files.
        class_file (str | Path | None, optional): Path to the class file. If not provided,
            attempts to find 'classes.txt', 'names.txt', or '.names' in the label directory.
        strict (bool, optional): If True, raise an error if no class file is found.
            Otherwise returns an empty iterator.

    Returns:
        Iterator[LabelImage]: Iterator over LabelImage instances.
    """
    if isinstance(label_dir, str):
        label_dir = Path(label_dir)
    if isinstance(class_file, str):
        class_file = Path(class_file)
    if class_file is None:
        candidates = ["classes.txt", "names.txt", ".names"]

        for candidate in candidates:
            class_file = label_dir.joinpath(candidate)
            if class_file.exists():
                break

    if class_file is None or not class_file.exists():
        if strict:
            raise ClassFileNotFoundError(label_dir.as_posix() + " | ".join(candidates))
        logger.debug("No Darknet class file found.")
        return iter([])

    classes = Darknet.load_class_file(class_file)
    return from_dir(img_dir, label_dir, Darknet(classes))


def write(filepath: str | Path, label_images: Iterable[LabelImage]) -> None:
    """
    Writes a list of LabelImage objects to a file in AAU JSON format.

    Args:
        filepath (str | Path): The path to the file where the LabelImage objects will be written.
        label_images (Iterable[LabelImage]): The list of LabelImage objects to be written.

    Returns:
        None
    """
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
    """
    Converts a list of LabelImage objects into a COCO dataset dictionary.

    Args:
        label_images (Iterable[LabelImage]): A list of LabelImage objects.
        license (COCOLicense): The license information for the dataset.
        info (COCOInfo): The info section of the COCO dataset.

    Returns:
        dict[str, Any]: A dictionary representing the COCO dataset.
    """
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
    """
    Converts a sequence of LabelImage objects into a pandas DataFrame.

    Parameters:
    label_images (Sequence[LabelImage]): A sequence of LabelImage objects.

    Returns:
    DataFrame: A pandas DataFrame containing the label image data.
    """
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
    """
    Converts a pandas DataFrame with the columns ["path", "image_width", "image_height", "x", "y", "label_width", "label_height", "classifier"]
    into an iterable of LabelImage objects.

    Parameters:
    df (DataFrame): A pandas DataFrame containing image data.

    Returns:
    Iterable[LabelImage]: An iterable of LabelImage objects.
    """

    # Old format uses 'classifier', new format uses 'name'
    if "classifier" in df:
        label_name = "classifier"
    else:
        label_name = "name"

    group_by = df.groupby(["path", "image_width", "image_height"])

    for (path, width, height), group in group_by:  # type: ignore
        labels: Sequence[Label] = [
            AAULabel(
                label["x"],  # type: ignore
                label["y"],  # type: ignore
                label["label_width"],  # type: ignore
                label["label_height"],  # type: ignore
                label[label_name],  # type: ignore
            )
            for _, label in group.iterrows()
        ]
        yield AAULabelImage(
            Path(path),
            width,
            height,
            labels,
        )  # type: ignore
