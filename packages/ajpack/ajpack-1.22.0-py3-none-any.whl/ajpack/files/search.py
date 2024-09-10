import os

def search_dir(dir: str, searchWord: str) -> list[tuple[str, int]]:
    files: list[str] = [os.path.join(dir, i) for i in os.listdir(dir) if os.path.isfile(os.path.join(dir, i))]
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