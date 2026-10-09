from __future__ import annotations

from rich.console import Console
from rich.text import Text


ORANGE = "#ff9a32"
YELLOW = "#ffd447"
TAGLINE = "Self-evolving harness units for agents."
LOOP_COLUMN = 34
BANNER = r"""
 _   _                             _
| | | |  __ _  _ __  _ __    ___  | |  ____  ____   _ __
| |_| | / _` || '__|| '_ \  / _ \ | | /    \/    \ | '_ \
|  _  || (_| || |   | | | ||  __/ | ||     /\     || |_) |
|_| |_| \__,_||_|   |_| |_| \___| |_| \___/  \___/ | .__/
                                                   |_|
""".strip("\n")
BANNER_WIDTH = max(len(line) for line in BANNER.splitlines())


def banner_text(width: int) -> Text:
    """Render the wordmark without changing the terminal's background."""
    if width < BANNER_WIDTH:
        compact = Text("Harne", style=ORANGE)
        compact.append("loop", style=YELLOW)
        return compact

    banner = Text(no_wrap=True)
    for index, line in enumerate(BANNER.splitlines()):
        if index:
            banner.append("\n")
        banner.append(line[:LOOP_COLUMN], style=ORANGE)
        banner.append(line[LOOP_COLUMN:], style=YELLOW)
    return banner


def print_banner(console: Console) -> None:
    console.print(banner_text(console.width))
    console.print(Text(TAGLINE, style=YELLOW))
    console.print()
