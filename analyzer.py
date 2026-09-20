import os
import sys
from pathlib import Path

CONFIG = {
    ".py": {"comment_single": "#", "block_start": '"""', "block_end": '"""'},
    ".cpp": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
    ".h": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
    ".js": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
    ".ts": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
}

def analyze_file(file_path: Path):
    ext = file_path.suffix
    if ext not in CONFIG:
        return None

    cfg = CONFIG[ext]
    total_lines = 0
    blank_lines = 0
    comment_lines = 0
    code_lines = 0

    in_block_comment = False

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total_lines += 1
                stripped = line.strip()

                # Пустая строка
                if not stripped:
                    blank_lines += 1
                    continue

                # Многострочные комментарии
                if cfg["block_start"] and cfg["block_end"]:
                    if not in_block_comment and stripped.startswith(cfg["block_start"]):
                        in_block_comment = True
                        comment_lines += 1
                        if stripped.endswith(cfg["block_end"]) and len(stripped) >= len(cfg["block_end"]):
                            in_block_comment = False
                        continue
                    elif in_block_comment:
                        comment_lines += 1
                        if stripped.endswith(cfg["block_end"]):
                            in_block_comment = False
                        continue

                # Однострочные комментарии
                if cfg["comment_single"] and stripped.startswith(cfg["comment_single"]):
                    comment_lines += 1
                else:
                    code_lines += 1

    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return None

    return {
        "file": file_path.name,
        "ext": ext,
        "total": total_lines,
        "code": code_lines,
        "comments": comment_lines,
        "blank": blank_lines,
    }

def scan_directory(root_dir: Path):
    results = []
    ignore_dirs = {".git", "build", "node_modules", "__pycache__", "venv", ".venv"}

    for path in root_dir.rglob("*"):
        if any(part in ignore_dirs for part in path.parts):
            continue
        if path.is_file():
            stats = analyze_file(path)
            if stats:
                results.append(stats)
    return results

def main():
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    
    if not target_dir.exists():
        print(f"Путь {target_dir} не существует!")
        return

    print( сканирование директории: {target_dir.resolve()} ...\n)
    data = scan_directory(target_dir)

    if not data:
        print("Подходящих файлов для анализа не найдено.")
        return

    # Вывод результатов
    print(f"{'Файл':<25} | {'Тип':<6} | {'Всего':<6} | {'Код':<6} | {'Коммент':<8} | {'Пустые':<6}")
    print("-" * 65)

    totals = {"total": 0, "code": 0, "comments": 0, "blank": 0}
    for row in data:
        print(f"{row['file']:<25} | {row['ext']:<6} | {row['total']:<6} | {row['code']:<6} | {row['comments']:<8} | {row['blank']:<6}")
        totals["total"] += row["total"]
        totals["code"] += row["code"]
        totals["comments"] += row["comments"]
        totals["blank"] += row["blank"]

    print("-" * 65)
    print(f"{'ИТОГО:':<25} | {'-':<6} | {totals['total']:<6} | {totals['code']:<6} | {totals['comments']:<8} | {totals['blank']:<6}")

if __name__ == "__main__":
    main()
