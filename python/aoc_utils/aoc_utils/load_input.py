from datetime import datetime
from pathlib import Path

def _get_repo_root():
    wd = Path.cwd()
    while not (wd / '.git').is_dir():
        if wd.root == wd:
            raise ValueError('Project root not found: not running in a git repository.')
        wd = wd.parent
    return wd
        
def open_input(day: int | None = None, year: int | None = None, postfix: str = ""):
    now = datetime.now()
    day = day or now.day
    year = year or now.year
    postfix = f'_{postfix}' if postfix else ""
    file_name = f'{year}_{day:02d}{postfix}.txt'
    input_file = _get_repo_root() / 'input' / file_name
    return open(input_file, encoding='utf-8')

def read_input_lines(day: int | None = None, year: int | None = None, postfix: str = "") -> list[str]:
    "Load lines of an input file (possibly having a postfix)."
    fp = open_input(day, year, postfix)
    lines = [line.strip() for line in fp.readlines()]
    fp.close()
    return lines

def read_input(day: int | None = None, year: int | None = None, postfix: str = ""):
    "Load text of an input file (possibly having a postfix)."
    fp = open_input(day, year, postfix)
    lines = fp.read()
    fp.close()
    return lines
