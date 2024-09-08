"""WebtoonScraper의 CLI 구현을 위한 코드들"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypeVar

from ..exceptions import InvalidPlatformError, InvalidURLError

if TYPE_CHECKING:
    from ..scrapers import Scraper
else:
    Scraper = None

platforms: dict[str, type[Scraper]] = {}


def _register(platform_name: str, scraper=None):
    if scraper is None:
        return lambda scraper: _register(platform_name, scraper)

    platforms[platform_name] = scraper
    return scraper


def instantiate(webtoon_platform: str, webtoon_id: str) -> Scraper:
    """웹툰 플랫폼 코드와 웹툰 ID로부터 스크레퍼를 인스턴스화하여 반환합니다. cookie, bearer 등의 추가적인 설정이 필요할 수도 있습니다."""

    Scraper: type[Scraper] | None = platforms.get(webtoon_platform.lower())  # type: ignore
    if Scraper is None:
        raise ValueError(f"Invalid webtoon platform: {webtoon_platform}")
    return Scraper._from_string(webtoon_id)


def instantiate_from_url(webtoon_url: str) -> Scraper:
    """웹툰 URL로부터 자동으로 알맞은 스크래퍼를 인스턴스화합니다. cookie, bearer 등의 추가적인 설정이 필요할 수 있습니다."""

    for PlatformClass in platforms.values():
        try:
            platform = PlatformClass.from_url(webtoon_url)
        except InvalidURLError:
            continue
        return platform
    raise InvalidPlatformError(f"Failed to retrieve webtoon platform from URL: {webtoon_url}")


def setup_instance(
    webtoon_id_or_url: str,
    webtoon_platform: str | Literal["url"],
    *,
    existing_episode_policy: Literal["skip", "raise", "download_again", "hard_check"] = "skip",
    cookie: str | None = None,
    download_directory: str | Path | None = None,
    options: dict[str, str] | None = None,
) -> Scraper:
    """여러 설정으로부터 적절한 스크래퍼 인스턴스를 반환합니다. CLI 사용을 위해 디자인되었습니다."""

    # 스크래퍼 불러오기
    if webtoon_platform == "url" or "." in webtoon_id_or_url:  # URL인지 확인
        scraper = instantiate_from_url(webtoon_id_or_url)
    else:
        scraper = instantiate(webtoon_platform, webtoon_id_or_url)

    # 부가 정보 불러오기
    if cookie:
        scraper.cookie = cookie
    if options:
        scraper._apply_options(options)

    # attribute 형식 설정 설정
    if download_directory:
        scraper.base_directory = download_directory
    scraper.existing_episode_policy = existing_episode_policy

    return scraper
