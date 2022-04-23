from pathlib import Path
from typing import Optional

staticBaseDir = Path('./static')
staticFileDir = staticBaseDir / 'dist'
staticFileDir.mkdir(parents=True, exist_ok=True)


def staticRef(path: Path, ref: Optional[Path] = None):
    if ref is None:
        ref = staticBaseDir
    return path.relative_to(ref)
