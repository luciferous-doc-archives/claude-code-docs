from os import environ, makedirs
from os.path import dirname

from utils.http import default_fetcher
from utils.logger import create_logger, logging_function
from utils.path import url_to_file_path

logger = create_logger(__name__)
BASE_DIR = "docs"


@logging_function(logger)
def main():
    base_timestamp = get_base_timestamp()
    url = "https://code.claude.com/llms.txt"
    content = default_fetcher(url=url)
    all_urls = parse_docs_urls(content)

    for url in all_urls:
        path = url_to_file_path(url=url, all_urls=all_urls)
        fetch_and_save(url=url, path=path, base_timestamp=base_timestamp)


@logging_function(logger)
def get_base_timestamp() -> str:
    return environ["BASE_TIMESTAMP"]


@logging_function(logger)
def parse_docs_urls(content: str) -> list[str]:
    lines = content.split("\n")
    urls = []
    in_docs_section = False

    for line in lines:
        if line.startswith("## Docs"):
            in_docs_section = True
            continue

        if in_docs_section:
            if line.startswith("##"):
                break

            line = line.strip()
            if not line:
                continue

            if line.startswith("- "):
                # "- [title](url): description" 形式を処理
                start = line.find("](")
                if start != -1:
                    end = line.find(")", start)
                    if end != -1:
                        url_part = line[start + 2 : end]
                        if not url_part.startswith(("http://", "https://")):
                            url_part = f"https://code.claude.com{url_part}"
                        urls.append(url_part)
            elif line.startswith(("http://", "https://")):
                urls.append(line.split()[0])

    return urls


@logging_function(logger)
def fetch_and_save(*, url: str, path: str, base_timestamp: str):
    file_path = f"{BASE_DIR}/claude-code-docs-{base_timestamp}/{path}"

    dir_path = dirname(file_path)
    makedirs(name=dir_path, exist_ok=True)

    markdown = default_fetcher(url=url)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)
