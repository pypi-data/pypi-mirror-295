from pathlib import Path

import pytest
from pytest import TempdirFactory

import aau_label

DATA_DIR = Path(__file__).parent.joinpath("data")


@pytest.fixture
def gomap_format_path():
    for path in DATA_DIR.joinpath("gomap_format").glob("*.json"):
        yield path


def test_from_file(gomap_format_path: Path):
    label_images = aau_label.from_file(gomap_format_path)
    assert isinstance(label_images, list), "label_images is not a list"


def test_write(gomap_format_path: Path, tmpdir_factory: TempdirFactory):
    file_name = Path(gomap_format_path.name)
    out = tmpdir_factory.mktemp("gomap_format_out").join(file_name)

    label_images = aau_label.from_file(gomap_format_path)
    aau_label.write(out.strpath, label_images)
    out.remove()
