from pathlib import Path

import funkify

from .main import cli
from .md import Markdown, recursive_read

__all__ = ['cli', 'Markdown', 'stream']

@funkify
def stream(file_or_content: str):
    if Path(file_or_content).exists():
        data = recursive_read(file_or_content)
    else:
        data = file_or_content.split("\n") if isinstance(file_or_content, str) else file_or_content
    md = Markdown(data=data)
    md.stream()
