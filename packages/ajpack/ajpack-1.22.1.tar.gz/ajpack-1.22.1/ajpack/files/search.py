import os

def search_dir(dir: str, searchWord: str, threads: int) -> list[tuple[str, int]]:
    files: list[str] = [os.path.join(root, file) for root, dirs, files in os.walk(dir) for file in files]
    found: list[tuple[str, int]] = []

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                for count, line in enumerate(f, 1):
                    if searchWord.lower() in line.lower():
                        found.append((file, count))
        except Exception as e:
            pass

    return found