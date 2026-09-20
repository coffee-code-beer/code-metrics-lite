# 📊 Code Metrics Lite

Лёгкая утилита на Python без внешних зависимостей для мгновенного анализа статистики кодовой базы и подсчета строк кода.

---

## 🧐 Что это такое?

**Code Metrics Lite** — это простой инструмент командной строки, состоящий всего из одного файла. Он создан для разработчиков, которым нужен быстрый обзор структуры проекта без установки тяжелых и громоздких систем анализа.

Независимо от того, работаете ли вы над бэкендом на Python, системным проектом на C++ или многоязычным пет-проектом, этот скрипт рекурсивно сканирует директорию, отделяет код от комментариев и пустых строк, а затем выводит чистую и аккуратную таблицу.

Поддерживаемые языки «из коробки»:
- Python (`.py`)
- C++ / C (`.cpp`, `.h`)
- JavaScript / TypeScript (`.js`, `.ts`)

---

## ✨ Особенности

- **Никаких зависимостей:** Использует только стандартные библиотеки Python (`os`, `sys`, `pathlib`). Никакой установки через `pip` не требуется (но опционально доступна).
- **Умный парсинг:** Различает реальные строки кода, однострочные комментарии и многострочные блоки комментариев.
- **Авто-игнорирование:** Автоматически пропускает стандартные служебные директории (`.git`, `build`, `node_modules`, `__pycache__`, `venv` и др.).
- **Активный вывод:** Формирует понятную терминальную таблицу со статистикой по каждому файлу и общим итогом.

---

## 🚀 Быстрый старт

### Вариант 1: Использование скачанного скрипта:
1. Скачайте или клонируйте скрипт (`analyzer.py`) в ваш рабочий каталог.
2. Запустите его через терминал, передав в качестве аргумента путь к нужной папке:

`python analyzer.py /path/to/your/project`

Если не указывать путь, скрипт автоматически проанализирует текущую рабочую директорию:

`python analyzer.py`

### Вариант 2: Установка через pip (прямо из GitHub):
Вы также можете установить утилиту глобально в систему одной командой:

`pip install git+https://github.com/coffee-code-beer/code-metrics-lite.git`.

В случае установки через `pip install` - используйте команду `code-metrics` для запуска утилиты. Также можно дополнительно указать путь или флаг.

---
### Использование .gitignore
Если вы хотите, чтобы скрипт также пропускал файлы и директории, указанные в .gitignore, добавьте аргумент `-gi` или `--gitignore` после пути к директории:
`python analyzer.py /path/to/your/project -gi`
или
`python analyzer.py /path/to/your/project --gitignore`
В этом режиме скрипт найдёт .gitignore в указанной директории и применит его правила при подсчёте строк.

Например, если в .gitignore указано:
```
node_modules/
build/
*.log
.env
```
то эти файлы и директории не будут учитываться в статистике.

Аргумент можно использовать и без указания пути:
`python analyzer.py --gitignore`
В этом случае будет проанализирована текущая директория с учётом её .gitignore.

Без аргумента `-gi` или `--gitignore` .gitignore не используется.

## 📊 Пример вывода

Сканирование директории: /home/user/projects/my-cpp-app ...
```
Файл                      | Тип    | Всего  | Код    | Коммент  | Пустые
-----------------------------------------------------------------
main.cpp                  | .cpp   | 145    | 110    | 20       | 15
utils.h                   | .h     | 42     | 30     | 8        | 4
config.py                 | .py    | 88     | 65     | 12       | 11
-----------------------------------------------------------------
ИТОГИ:                    | -      | 275    | 205    | 40       | 30
```
При использовании --gitignore файлы, исключённые через .gitignore, не появятся в таблице и не будут включены в итоговое количество строк.

---

## 🛠️ Расширение

Хотите добавить поддержку другого языка программирования? Просто откройте файл analyzer.py и добавьте новую запись в словарь CONFIG в самом начале файла:

---

## 🤝 Участие в разработке

Контрибьюты, исправления и предложения новых функций горячо приветствуются! Смело заглядывайте на страницу issues.
---

## 📝 Лицензия

Этот проект распространяется под открытой лицензией MIT License.

<br>
<br>
<br>

# 📊 Code Metrics Lite

A small Python tool with no external dependencies for quickly checking code statistics and counting lines of code.

---

## 🧐 What is it?

**Code Metrics Lite** is a simple command-line tool made from just one file. It is made for developers who want a quick look at their project without installing large code analysis tools.

Whether you are working on a Python backend, a C++ project, or a small multi-language project, the script scans the directory recursively, separates code from comments and empty lines, and prints a clean table.

Supported languages out of the box:
- Python (`.py`)
- C++ / C (`.cpp`, `.h`)
- JavaScript / TypeScript (`.js`, `.ts`)

---

## ✨ Features

-No dependencies: Uses only Python's standard library (os, sys, pathlib). No pip installation is required.
- Simple parsing: Separates code lines, single-line comments, and multi-line comment blocks.
- Automatic ignores: Automatically skips common folders such as .git, build, node_modules, __pycache__, venv, and others.
- .gitignore support: With the -gi or --gitignore argument, the script also reads .gitignore rules and skips the files and folders listed there.
- Clear output: Shows a simple terminal table with statistics for each file and the total.

---

## 🚀 Quick Start

### Option 1: Run the downloaded script:
1. Download or clone the script (analyzer.py) into your working directory.
2. Run it from the terminal and give it the path to the project you want to analyze:

`python analyzer.py /path/to/your/project`

If you do not give a path, the script will analyze the current directory:

`python analyzer.py`

### Option 2: Installation via pip (directly from GitHub):
You can also install the utility globally to the system with one command:

`pip install git+https://github.com/coffee-code-beer/code-metrics-lite.git`

After installing via `pip`, use the `code-metrics` command to run the utility. You can also specify a path or flag if needed.

---
### Using .gitignore
If you want the script to also skip files and folders listed in .gitignore, add `-gi` or `--gitignore` after the directory path:
`python analyzer.py /path/to/your/project -gi`
or:
`python analyzer.py /path/to/your/project --gitignore`
In this mode, the script will find the .gitignore file in the selected directory and use its rules while counting lines.

For example, if your .gitignore contains:
```
node_modules/
build/
*.log
.env
```
these files and folders will not be included in the statistics.

You can also use the argument without specifying a path:
`python analyzer.py --gitignore`
In this case, the current directory will be analyzed using its .gitignore.

Without `-gi` or `--gitignore`, the .gitignore file is not used.

## 📊 Example Output

Scanning directory: /home/user/projects/my-cpp-app ...
```
Файл                      | Тип    | Всего  | Код    | Коммент  | Пустые
-----------------------------------------------------------------
main.cpp                  | .cpp   | 145    | 110    | 20       | 15
utils.h                   | .h     | 42     | 30     | 8        | 4
config.py                 | .py    | 88     | 65     | 12       | 11
-----------------------------------------------------------------
ИТОГИ:                    | -      | 275    | 205    | 40       | 30
```
When --gitignore is used, files excluded by .gitignore will not appear in the table and will not be included in the total line count.

---

## 🛠️ Extending the Tool

Want to add support for another programming language?

Just open analyzer.py and add a new entry to the CONFIG dictionary at the top of the file.

---

## 🤝 Contributing

Contributions, bug fixes, and ideas for new features are welcome!

Feel free to check the Issues page.

---

## 📝 License

This project is released under the MIT License.
