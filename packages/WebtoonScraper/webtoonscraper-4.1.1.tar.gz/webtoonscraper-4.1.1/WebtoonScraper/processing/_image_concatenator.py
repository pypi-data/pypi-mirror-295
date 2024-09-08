from __future__ import annotations

import os
import shutil
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Literal

from tqdm import tqdm

from WebtoonScraper.exceptions import MissingOptionalDependencyError

from ..base import DEFAULT_PROCESS_NUMBER, logger
from ._viewer import add_viewer
from .directory_merger import ContainerStates, _directories_and_files_of, ensure_normal

BatchMode = tuple[Literal["count", "height"], int] | tuple[Literal["ratio"], float] | Literal["all"]

if TYPE_CHECKING:
    from PIL import Image, UnidentifiedImageError
else:
    Image = UnidentifiedImageError = None


def _load_pillow():
    global Image, UnidentifiedImageError
    if Image is None:
        with MissingOptionalDependencyError.importing("Pillow", "concat"):
            from PIL import Image
    if UnidentifiedImageError is None:
        with MissingOptionalDependencyError.importing("Pillow", "concat"):
            from PIL import UnidentifiedImageError


def concat_webtoon(
    source_webtoon_directory: Path,
    target_webtoon_directory: Path | None,
    batch: BatchMode,
    rebuild_webtoon_viewer: bool = True,
    manual_container_state: ContainerStates | None = None,
    thread_number: int | None = None,
    use_progress_bar: bool = True,
) -> Path:
    """여러 그림 파일을 하나로 연결합니다.

    Args:
        source_webtoon_directory: 연결할 사진 파일이 있는 에피소드를 포함하는 웹툰 디렉토리입니다.
        target_webtoon_directory: 결과물을 저장할 웹툰 디렉토리입니다.
            만약에 None이면 자동으로 이름을 선정하는데, 예를 들어 디렉토리 이름이
            `webtoon(webtoon_id)`이면 `webtoon(webtoon_id, concatenated)`로 설정합니다.
        batch_size: 하나로 연결하는 방식의 기준입니다.
        batch_mode: 어떤 수치를 기준으로 그림을 묶을지 결정합니다.
            batch_size가 -1이면 모드에 상관없이 전체를 묶습니다.
            * 만약 "count"이면 그림 개수를 기준으로 결정됩니다.
                예를 들어 batch_size가 3이라면 그림 파일 3개를 한 파일로 연결합니다.
            * 만약 "height"이면 그림의 총 세로 픽셀 수로 결정합니다.
                예를 들어 batch_size가 8000이면 그림 파일의 세로 픽셀 수가 최소 8000이 되도록
                한 파일로 연결합니다. 이때 해당 에피소드의 마지막 파일은 8000보다 작을 수 있으며 멱등적입니다.
            * 만약 "ratio"이면 `세로 픽셀 수 / 가로 픽셀 수`를 기준으로 파일을 연결합니다.
                예를 들어 batch_size가 `11.5`이면 `세로 픽셀 수 / 가로 픽셀 수`가 11.5와 같거나 크도록
                한 파일로 연결됩니다. 이때 해당 에피소드의 마지막 파일은 8000보다 작을 수 있으며 멱등적입니다.
        rebuild_webtoon_viewer: 이미지를 연결하면 기존의 웹툰 뷰어를 사용할 수 없습니다.
            이 옵션을 켜면 웹툰 뷰어를 사용할 수 있도록 다시 만듭니다.
        thread_number: 멀티프로세싱을 활용하여 더욱 빠르게 작업을 수행합니다.
            thread_number가 1이라면 멀티프로세싱을 활용하지 않습니다.
            만약 멀티프로세싱을 안전하게 사용할 수 없는 환경이라면 1로 설정하세요.

    Returns:
        연결된 이미지들이 들어 있는 웹툰 디렉토리를 반환합니다. 만약 WORKING 파일로 인해 비정상 종료되었다면 None을 반환합니다.
    """
    ensure_normal(source_webtoon_directory, empty_ok=False, manual_container_state=manual_container_state)

    directories, files = _directories_and_files_of(source_webtoon_directory)

    if target_webtoon_directory is None:
        name = source_webtoon_directory.name
        if name.endswith(")"):
            target_name = name.removesuffix(")") + ", concatenated)"
        else:
            target_name = name + "(concatenated)"
        target_webtoon_directory = source_webtoon_directory.parent / target_name

    target_webtoon_directory.mkdir(parents=True, exist_ok=True)

    # 멀티스레딩 활용하지 않음
    if thread_number == 1:
        if use_progress_bar:
            directories = tqdm(directories, total=len(directories))

        for i, episode_directory in enumerate(directories, 1):
            episode_name = episode_directory.name
            target = target_webtoon_directory / episode_name
            _concat_episode(episode_directory, target, batch)

            if use_progress_bar:
                if TYPE_CHECKING:
                    assert isinstance(directories, tqdm)
                directories.set_description(f"Episode {episode_name} concatenation ended")
            else:
                logger.info(f"[{i:02d}/{len(directories):02d}] Episode {episode_name} concatenation ended")

    # 멀티스레딩 활용
    else:
        parameters = [
            (episode_directory, target_webtoon_directory / episode_directory.name, batch)
            for episode_directory in directories
        ]

        with ThreadPool(thread_number or DEFAULT_PROCESS_NUMBER) as p:
            directory_names = p.imap_unordered(_concat_episode_packed, parameters)  # type: ignore

            if use_progress_bar:
                progress_bar = tqdm(directory_names, total=len(parameters))
                for episode_name in progress_bar:
                    progress_bar.set_description(f"Episode {episode_name} concatenation ended")
            else:
                for i, episode_name in enumerate(directory_names, 1):
                    logger.info(f"[{i:02d}/{len(parameters):02d}] Episode {episode_name} concatenation ended")

    for file in files:
        shutil.copy(file, target_webtoon_directory / file.name)

    if rebuild_webtoon_viewer:
        add_viewer(target_webtoon_directory)

    return target_webtoon_directory


def _concat_episode_packed(args: tuple[Path, Path, BatchMode]):
    _concat_episode(*args)
    return args[1].name  # Directory name


def _concat_episode(
    source_episode_directory: Path,
    target_episode_directory: Path,
    batch: BatchMode,
) -> None:
    _load_pillow()  # concat_webtoon에 이 옵션을 사용하면 multiprocessing을 이용할 때 문제가 발생할 수 있음!!

    target_episode_directory.mkdir(exist_ok=True)

    image_names = sorted(os.listdir(source_episode_directory))
    match batch:
        case "all":
            fetcher = _get_images_by_count(source_episode_directory, image_names, -1)

        case "count", int(count):
            fetcher = _get_images_by_count(source_episode_directory, image_names, count)

        case "height", int(height):
            fetcher = _get_images_by_height(source_episode_directory, image_names, height)

        case "ratio", (int(ratio) | float(ratio)):
            fetcher = _get_images_by_ratio(source_episode_directory, image_names, ratio)

        case _:
            raise ValueError(f"Unknown batch mode or invalid type. batch: {batch}")

    for i, images in enumerate(fetcher):
        if not images:
            continue

        if len(images) == 1:
            (image,) = images
            image.save(target_episode_directory / f"{i:03d}.jpg", optimize=True, quality=95)
            image.close()
            continue

        width = max(image.width for image in images)
        height = sum(image.height for image in images)

        y = 0
        with Image.new("RGB", (width, height)) as composite:
            for image in images:
                composite.paste(image, (0, y))
                y += image.height

            composite.save(target_episode_directory / f"{i:03d}.jpg", optimize=True, quality=95)

        for image in images:
            image.close()


def _get_images_by_count(directory: Path, image_names: list[str], count: int) -> Iterator[list[Image.Image]]:
    result: list[Image.Image] = []
    pointer = goal = 0
    while pointer < len(image_names):
        while goal and pointer < len(image_names) and pointer < goal:
            image_dir = directory / image_names[pointer]

            try:
                result.append(Image.open(image_dir))
            except UnidentifiedImageError:
                # 이미지가 아니어서 실패할 경우 오류를 내는 것이 아닌 해당 이미지를 무시하고
                # 다음 이미지를 불러오는 것을 시도함.
                continue

            pointer += 1

        yield result
        if count == -1:
            count = len(image_names)
        goal = pointer + count
        result.clear()


def _get_images_by_height(directory: Path, image_names: list[str], height: int) -> Iterator[list[Image.Image]]:
    result: list[Image.Image] = []
    pointer = sum_of_image_height = 0
    while pointer < len(image_names):
        while pointer < len(image_names) and (height == -1 or sum_of_image_height < height):
            image_dir = directory / image_names[pointer]

            try:
                image = Image.open(image_dir)
            except UnidentifiedImageError:
                # 이미지가 아니어서 실패할 경우 오류를 내는 것이 아닌 해당 이미지를 무시하고
                # 다음 이미지를 불러오는 것을 시도함.
                continue
            else:
                result.append(image)
                sum_of_image_height += image.height

            pointer += 1

        sum_of_image_height = 0
        yield result
        result.clear()


def _get_images_by_ratio(directory: Path, image_names: list[str], ratio: int | float) -> Iterator[list[Image.Image]]:
    result: list[Image.Image] = []
    pointer = sum_of_image_height = image_width = 0
    while pointer < len(image_names):
        while (
            pointer < len(image_names)
            and ratio
            and (ratio == -1 or image_width == 0 or sum_of_image_height / image_width < ratio)
        ):
            image_dir = directory / image_names[pointer]

            try:
                image = Image.open(image_dir)
            except UnidentifiedImageError:
                # 이미지가 아니어서 실패할 경우 오류를 내는 것이 아닌 해당 이미지를 무시하고
                # 다음 이미지를 불러오는 것을 시도함.
                continue
            else:
                result.append(image)
                sum_of_image_height += image.height
                image_width = max(image_width, image.width)

            pointer += 1

        sum_of_image_height = 0
        image_width = 0
        yield result
        result.clear()
