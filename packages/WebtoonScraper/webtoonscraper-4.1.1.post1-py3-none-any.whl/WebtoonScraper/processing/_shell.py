import shlex
from contextlib import suppress

from WebtoonScraper.__main__ import main as WebtoonScraperMain
from WebtoonScraper import __version__


def main():
    print(f"WebtoonScraper {__version__}")
    with suppress(BaseException):
        WebtoonScraperMain(["--help"])
    print()
    print("Type 'exit' or press ctrl+C to quit")
    while True:
        # EOFError를 놔두기 위해 input은 suppress로 감싸지 않음.
        command = input(">>> ")
        if command == "exit":
            break

        with suppress(BaseException):
            # 잘못된 구문을 만났을 경우에도 튕기지 않기 위해
            # shlex.split도 suppress로 감쌈.
            args = shlex.split(command)
            if args[0].lower() in {"webtoon", "webtoonscraper"}:
                del args[0]
            WebtoonScraperMain(args)


if __name__ == "__main__":
    main()
