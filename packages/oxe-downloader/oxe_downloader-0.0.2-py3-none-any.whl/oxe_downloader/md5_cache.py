import hashlib
from pathlib import Path


def get_md5_path(path: Path) -> Path:
    return path.parent / ".md5_cache" / (path.name + ".md5")


def check_md5_valid(path: Path) -> bool:
    # check if an md5 hash file exists
    md5_path = get_md5_path(path)

    if not md5_path.exists():
        return False
    if not md5_path.is_file():
        return False
    # check if the md5 is older than the file
    if md5_path.stat().st_mtime < path.stat().st_mtime:
        return False
    
    return True


def cached_md5_hash(path: Path) -> bytes:
    # check if an md5 hash file exists
    need_new_md5 = not check_md5_valid(path)
    md5_path = get_md5_path(path)

    if need_new_md5:
        # read the file and hash it
        with path.open("rb") as f:
            md5 = hashlib.md5(f.read()).digest()
        # write the hash to a file
        md5_path = get_md5_path(path)
        md5_path.parent.mkdir(parents=True, exist_ok=True)
        # Overwrite whatever is there
        with md5_path.open("wb") as f:
            f.write(md5)

    return md5_path.read_bytes()
