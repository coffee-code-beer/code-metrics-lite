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

                if not stripped:
                    blank_lines += 1
                    continue

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

                if cfg["comment_single"] and stripped.startswith(cfg["comment_single"]):
                    comment_lines += 1
                else:
                    code_lines += 1

    except (OSError, PermissionError) as e:
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

def print_table(headers: list, rows: list):
    if not rows:
        return

    MAX_FILE_LEN = 40
    
    col_widths = [len(h) for h in headers]
    for r in rows:
        file_len = min(len(r[0]), MAX_FILE_LEN)
        if file_len > col_widths[0]:
            col_widths[0] = file_len
        
        for i in range(1, len(r)):
            if len(r[i]) > col_widths[i]:
                col_widths[i] = len(r[i])

    def format_row(r):
        file_name = r[0]
        if len(file_name) > MAX_FILE_LEN:
            file_name = file_name[:MAX_FILE_LEN - 3] + "..."
        
        formatted = [
            f"{file_name:<{col_widths[0]}}",
            f"{r[1]:<{col_widths[1]}}",
            f"{r[2]:>{col_widths[2]}}",
            f"{r[3]:>{col_widths[3]}}",
            f"{r[4]:>{col_widths[4]}}",
            f"{r[5]:>{col_widths[5]}}"
        ]
        return " | ".join(formatted)

    header_parts = [
        f"{h:>{col_widths[i]}}" if i >= 2 else f"{h:<{col_widths[i]}}"
        for i, h in enumerate(headers)
    ]
    header_str = " | ".join(header_parts)
    separator = "-" * len(header_str)

    print(header_str)
    print(separator)
    for r in rows[:-1]:
        print(format_row(r))
    print(separator)
    print(format_row(rows[-1]))

def main():
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    
    if not target_dir.exists():
        print(f"Путь {target_dir} не существует!")
        return

    print(f"Сканирование директории: {target_dir.resolve()} ...\n")
    data = scan_directory(target_dir)

    if not data:
        print("Подходящих файлов для анализа не найдено.")
        return

    headers = ["Файл", "Тип", "Всего", "Код", "Коммент", "Пустые"]
    rows = []
    totals = {"total": 0, "code": 0, "comments": 0, "blank": 0}

    for row in data:
        rows.append([
            str(row['file']),
            str(row['ext']),
            str(row['total']),
            str(row['code']),
            str(row['comments']),
            str(row['blank'])
        ])
        totals["total"] += row["total"]
        totals["code"] += row["code"]
        totals["comments"] += row["comments"]
        totals["blank"] += row["blank"]

    rows.append([
        "ИТОГО:",
        "-",
        str(totals["total"]),
        str(totals["code"]),
        str(totals["comments"]),
        str(totals["blank"])
    ])

    print_table(headers, rows)

if __name__ == "__main__":
    main()
