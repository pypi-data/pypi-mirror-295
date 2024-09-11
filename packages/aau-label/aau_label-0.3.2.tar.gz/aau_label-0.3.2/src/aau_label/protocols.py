from pathlib import Path
from typing import ClassVar, Protocol, Sequence

from PIL.Image import Image
from typing_extensions import deprecated


class Label(Protocol):
    x: int
    y: int
    width: int
    height: int
    name: str


class LabelImage(Protocol):
    path: Path
    width: int
    height: int
    labels: Sequence[Label]


@deprecated("Use LabelImageDeserializer instead")
class LabelParser(Protocol):
    file_extension: ClassVar[str]

    def parse(self, label_file: Path, image: Image) -> Sequence[Label]:
        raise NotImplementedError


class LabelImageDeserializer(Protocol):
    file_extension: ClassVar[str]

    def deserialize(
        self, img_file: Path, label_file: Path, image: Image | None = None
    ) -> LabelImage:
        raise NotImplementedError


class LabelImageSerializer(Protocol):
    def serialize(self, label: LabelImage) -> str:
        raise NotImplementedError
