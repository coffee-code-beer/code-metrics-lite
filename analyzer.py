import argparse
import fnmatch
from pathlib import Path

CONFIG = {
    ".py": {"comment_single": "#", "block_start": '"""', "block_end": '"""'},
    ".cpp": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
    ".h": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
    ".js": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
    ".ts": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
    ".jsx": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
    ".tsx": {"comment_single": "//", "block_start": "/*", "block_end": "*/"},
}

class GitignoreRule:
    def __init__(self, pattern: str):
        self.original = pattern
        self.negated = False
        self.directory_only = False
        self.anchored = False

        if pattern.startswith("!"):
            self.negated = True
            pattern = pattern[1:]
        elif pattern.startswith(r"\!"):
            pattern = pattern[1:]

        if pattern.endswith("/"):
            self.directory_only = True
            pattern = pattern.rstrip("/")

        if pattern.startswith("/"):
            self.anchored = True
            pattern = pattern[1:]
        elif "/" in pattern:
            self.anchored = True

        self.pattern = pattern

    def matches(self, rel_path: str, is_dir: bool) -> bool:
        if not self.pattern:
            return False

        if self.directory_only and not is_dir:
            return False

        if not self.anchored:
            parts = rel_path.split("/")
            for part in parts:
                if fnmatch.fnmatchcase(part, self.pattern):
                    return True
            return fnmatch.fnmatchcase(rel_path, self.pattern)

        return self._match_path(rel_path, self.pattern)

    @staticmethod
    def _match_path(path: str, pattern: str) -> bool:
        if "**" not in pattern:
            return fnmatch.fnmatchcase(path, pattern)

        # Простая обработка wildcard **
        if pattern.startswith("**/"):
            suffix = pattern[3:]
            if fnmatch.fnmatchcase(path, suffix):
                return True
            parts = path.split("/")
            for i in range(1, len(parts)):
                if fnmatch.fnmatchcase("/".join(parts[i:]), suffix):
                    return True
            return False

        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            return path == prefix or path.startswith(prefix + "/")

        parts = pattern.split("**")
        if len(parts) == 2:
            left, right = parts[0].strip("/"), parts[1].strip("/")
            path_parts = path.split("/")
            for i in range(len(path_parts) + 1):
                left_part = "/".join(path_parts[:i])
                right_part = "/".join(path_parts[i:])
                left_ok = not left or fnmatch.fnmatchcase(left_part, left)
                right_ok = not right or fnmatch.fnmatchcase(right_part, right)
                if left_ok and right_ok:
                    return True

        return fnmatch.fnmatchcase(path, pattern)


class Gitignore:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()
        self.rules = []

        gitignore_path = self.root_dir / ".gitignore"
        if not gitignore_path.is_file():
            return

        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.rstrip("\r\n").strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith(r"\#"):
                        line = line[1:]
                    self.rules.append(GitignoreRule(line))
        except (OSError, PermissionError) as e:
            print(f"Ошибка при чтении .gitignore: {e}")

    def _relative_path(self, path: Path) -> str | None:
        try:
            relative = path.resolve().relative_to(self.root_dir)
            return relative.as_posix()
        except ValueError:
            return None

    def is_ignored(self, path: Path) -> bool:
        rel_path = self._relative_path(path)
        if rel_path is None:
            return False

        if rel_path == ".gitignore":
            return True

        is_dir = path.is_dir()
        parts = rel_path.split("/")
        
        ignored = False

        for rule in self.rules:
            match_found = False
            curr_subpath = ""
            
            for i in range(len(parts)):
                part = parts[i]
                curr_subpath = f"{curr_subpath}/{part}" if curr_subpath else part
                is_subpath_dir = (i < len(parts) - 1) or is_dir

                if rule.matches(curr_subpath, is_subpath_dir):
                    match_found = True
                    break

            if match_found:
                ignored = not rule.negated

        return ignored


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

                if ext in (".jsx", ".tsx"):
                    if stripped.startswith("{/*") and stripped.endswith("*/}"):
                        comment_lines += 1
                        continue
                    
                    if not in_block_comment and stripped.startswith("{/*"):
                        in_block_comment = True
                        comment_lines += 1
                        continue

                    if in_block_comment and stripped.endswith("*/}"):
                        in_block_comment = False
                        comment_lines += 1
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

def scan_directory(root_dir: Path, use_gitignore=False):
    results = []
    ignore_dirs = {".git", "__pycache__", "venv", ".venv"}
    gitignore = Gitignore(root_dir) if use_gitignore else None

    import os

    for current_dir, dirs, files in os.walk(root_dir):
        current_path = Path(current_dir)

        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        if gitignore:
            filtered_dirs = []
            for dirname in dirs:
                dir_path = current_path / dirname
                if not gitignore.is_ignored(dir_path):
                    filtered_dirs.append(dirname)
            dirs[:] = filtered_dirs

        for filename in files:
            file_path = current_path / filename

            if gitignore and gitignore.is_ignored(file_path):
                continue

            stats = analyze_file(file_path)
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
    parser = argparse.ArgumentParser(
        description="Анализ количества строк кода, комментариев и пустых строк."
    )

    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Директория для сканирования (по умолчанию текущая)"
    )

    parser.add_argument(
        "-gi",
        "--gitignore",
        action="store_true",
        help="Использовать .gitignore из корневой директории"
    )

    args = parser.parse_args()
    target_dir = Path(args.target_dir)

    if not target_dir.exists():
        print(f"Путь {target_dir} не существует!")
        return

    if not target_dir.is_dir():
        print(f"Путь {target_dir} не является директорией!")
        return

    print(f"Сканирование директории: {target_dir.resolve()} ...")

    if args.gitignore:
        gitignore_path = target_dir / ".gitignore"
        if gitignore_path.is_file():
            print("Используется .gitignore")
        else:
            print(".gitignore не найден, используется стандартный список исключений.")

    print()

    data = scan_directory(target_dir, use_gitignore=args.gitignore)

    if not data:
        print("Подходящих файлов для анализа не найдено.")
        return

    headers = ["Файл", "Тип", "Всего", "Код", "Коммент", "Пустые"]
    rows = []

    totals = {"total": 0, "code": 0, "comments": 0, "blank": 0}

    for row in data:
        rows.append([
            str(row["file"]),
            str(row["ext"]),
            str(row["total"]),
            str(row["code"]),
            str(row["comments"]),
            str(row["blank"])
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
