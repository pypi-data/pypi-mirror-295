import re
import unicodedata

UNICODE_NORM_FORM = "NFKC"
WHITESPACE_RE = re.compile(r"\s+")


def preprocess_text(text: str, language: str = None, *, normalize: bool = False) -> str:
    if normalize:
        text = unicodedata.normalize(UNICODE_NORM_FORM, text)
    text = collapse_whitespace(text)
    return text


def collapse_whitespace(text):
    text = re.sub(WHITESPACE_RE, " ", text)
    return text


def intersperse(lst, item):
    # Adds blank symbol
    result = [item] * (len(lst) * 2 + 1)
    result[1::2] = lst
    return result
