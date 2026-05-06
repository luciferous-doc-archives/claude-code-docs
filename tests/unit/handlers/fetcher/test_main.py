import pytest

from handlers.fetcher.main import parse_docs_urls


class TestParseDocsUrls:
    def test_parse_markdown_link_single_url(self):
        content = """
## Docs

- [Documentation](https://example.com/docs): Main documentation
"""
        result = parse_docs_urls(content)
        assert result == ["https://example.com/docs"]

    def test_parse_markdown_link_multiple_urls(self):
        content = """
## Docs

- [Doc1](https://example.com/doc1): First documentation
- [Doc2](https://example.com/doc2): Second documentation
- [Doc3](https://example.com/doc3): Third documentation
"""
        result = parse_docs_urls(content)
        assert result == [
            "https://example.com/doc1",
            "https://example.com/doc2",
            "https://example.com/doc3",
        ]

    def test_parse_direct_url_format(self):
        content = """
## Docs

https://example.com/direct-doc
https://example.com/another-doc
"""
        result = parse_docs_urls(content)
        assert result == [
            "https://example.com/direct-doc",
            "https://example.com/another-doc",
        ]

    def test_parse_relative_url_with_prefix(self):
        content = """
## Docs

- [Relative Doc](/docs/relative): Relative path documentation
"""
        result = parse_docs_urls(content)
        assert result == ["https://code.claude.com/docs/relative"]

    def test_parse_mixed_absolute_and_relative(self):
        content = """
## Docs

- [Absolute](https://external.com/doc): Absolute link
- [Relative](/docs/local): Relative link
"""
        result = parse_docs_urls(content)
        assert result == [
            "https://external.com/doc",
            "https://code.claude.com/docs/local",
        ]

    def test_parse_only_docs_section(self):
        content = """
## Overview

- [Overview Link](https://example.com/overview): Should be ignored

## Docs

- [Docs Link](https://example.com/docs): Should be included

## FAQ

- [FAQ Link](https://example.com/faq): Should be ignored
"""
        result = parse_docs_urls(content)
        assert result == ["https://example.com/docs"]

    def test_parse_empty_docs_section(self):
        content = """
## Docs

## Next Section
"""
        result = parse_docs_urls(content)
        assert result == []

    def test_parse_docs_section_with_empty_lines(self):
        content = """
## Docs

- [Doc1](https://example.com/doc1): First

- [Doc2](https://example.com/doc2): Second

- [Doc3](https://example.com/doc3): Third
"""
        result = parse_docs_urls(content)
        assert result == [
            "https://example.com/doc1",
            "https://example.com/doc2",
            "https://example.com/doc3",
        ]

    def test_parse_docs_section_not_found(self):
        content = """
## Overview

- [Overview Link](https://example.com/overview)

## FAQ

- [FAQ Link](https://example.com/faq)
"""
        result = parse_docs_urls(content)
        assert result == []

    def test_parse_direct_url_with_query_params(self):
        content = """
## Docs

https://example.com/doc?param=value&other=123
"""
        result = parse_docs_urls(content)
        assert result == ["https://example.com/doc?param=value&other=123"]

    def test_parse_direct_url_with_trailing_spaces(self):
        content = """
## Docs

https://example.com/doc-with-spaces
https://example.com/another
"""
        result = parse_docs_urls(content)
        assert result == [
            "https://example.com/doc-with-spaces",
            "https://example.com/another",
        ]

    def test_parse_markdown_link_with_special_chars_in_url(self):
        content = """
## Docs

- [Complex URL](https://example.com/path/to/doc-with-dashes_and_underscores): Complex path
"""
        result = parse_docs_urls(content)
        assert result == ["https://example.com/path/to/doc-with-dashes_and_underscores"]

    def test_parse_stops_at_next_section(self):
        content = """
## Docs

- [Doc1](https://example.com/doc1): First

## Resources

- [Resource1](https://example.com/resource1): Should not be included
"""
        result = parse_docs_urls(content)
        assert result == ["https://example.com/doc1"]

    def test_parse_mixed_formats_in_same_section(self):
        content = """
## Docs

- [Markdown Link](https://example.com/markdown): Markdown format
https://example.com/direct
- [Another Markdown](/relative/path): Relative path
"""
        result = parse_docs_urls(content)
        assert result == [
            "https://example.com/markdown",
            "https://example.com/direct",
            "https://code.claude.com/relative/path",
        ]

    def test_parse_http_protocol(self):
        content = """
## Docs

- [HTTP Doc](http://example.com/doc): HTTP protocol
- [HTTPS Doc](https://example.com/doc): HTTPS protocol
"""
        result = parse_docs_urls(content)
        assert result == [
            "http://example.com/doc",
            "https://example.com/doc",
        ]

    def test_parse_ignores_non_link_lines(self):
        content = """
## Docs

This is a comment line that should be ignored
- [Valid Link](https://example.com/doc): Valid link
Another non-link line
"""
        result = parse_docs_urls(content)
        assert result == ["https://example.com/doc"]

    def test_parse_handles_malformed_markdown_link(self):
        content = """
## Docs

- Missing closing bracket: Not a valid markdown link
- [Valid Link](https://example.com/valid): Valid
- Broken pattern text
"""
        result = parse_docs_urls(content)
        # The malformed links should be ignored, only valid one extracted
        assert result == ["https://example.com/valid"]

    def test_parse_relative_url_with_leading_slash(self):
        content = """
## Docs

- [Root Relative](/docs): Root relative path
- [File Relative](/docs/path): File relative path with leading slash
"""
        result = parse_docs_urls(content)
        assert result == [
            "https://code.claude.com/docs",
            "https://code.claude.com/docs/path",
        ]
