from utils.http import default_fetcher
from utils.logger import create_logger, logging_function

logger = create_logger(__name__)


@logging_function(logger)
def main():
    url = "https://code.claude.com/llms.txt"
    content = default_fetcher(url=url)
    docs_urls = parse_docs_urls(content)

    logger.info(
        f"Docs配下のURLを抽出しました",
        extra={"count": len(docs_urls), "urls": docs_urls},
    )


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
