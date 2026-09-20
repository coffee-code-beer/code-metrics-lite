# 📊 Code Metrics Lite

A lightweight, zero-dependency Python utility for instant codebase statistics and line counting.

---

## 🧐 What is this?

**Code Metrics Lite** is a simple, single-file command-line tool designed for developers who want a quick overview of their project's structure without installing heavy, bloated analysis tools. 

Whether you are working on a Python backend, a C++ systems project, or a multi-language pet project, this script recursively scans your directory, separates code from comments and blank lines, and outputs a clean, formatted table.

Supported languages out of the box:
- Python (.py)
- C++ / C (.cpp, .h)
- JavaScript / TypeScript (.js, .ts)

---

## ✨ Features

- **Zero Dependencies:** Uses only Python standard libraries (os, sys, pathlib). No pip install required!
- **Smart Parsing:** Distinguishes between actual code lines, single-line comments, and multi-line/block comments.
- **Auto-Ignition:** Automatically skips common clutter directories (.git, build, node_modules, __pycache__, venv, etc.).
- **Clean Output:** Renders a neat terminal table with file-by-file stats and a grand total summary.

---

## 🚀 Quick Start

1. Download or clone the script (analyzer.py) into your workspace.
2. Run it via your terminal, passing the target directory path as an argument:

python analyzer.py /path/to/your/project

If you don't specify a path, it will automatically analyze the current working directory:

python analyzer.py

---

## 📊 Example Output

 Сканирование директории: /home/user/projects/my-cpp-app ...

Файл                      | Тип    | Всего  | Код    | Коммент  | Пустые
-----------------------------------------------------------------
main.cpp                  | .cpp   | 145    | 110    | 20       | 15
utils.h                   | .h     | 42     | 30     | 8        | 4
config.py                 | .py    | 88     | 65     | 12       | 11
-----------------------------------------------------------------
ИТОГИ:                    | -      | 275    | 205    | 40       | 30

---

## 🛠️ Extending

Want to add support for another language? Just open analyzer.py and add a new entry to the CONFIG dictionary at the top of the file.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---

## 📝 License

This project is open-source under the MIT License.
