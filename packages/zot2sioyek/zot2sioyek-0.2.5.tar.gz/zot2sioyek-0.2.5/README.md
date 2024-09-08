# Zotero to Sioyek Highlights Manager

---

**Python script to embed zotero highlights to [sioyek](https://github.com/ahrm/sioyek), and other utils.**

- 🐍 Python [sqlite3](https://docs.python.org/3/library/sqlite3.html) and [pyzotero](https://github.com/urschrei/pyzotero) Based Script

> [!WARNING] > **Tested only in linux**

[![updatebadge]][update] [![pypibadge]][pypi] [![mitbadge]][license]

[![ruffbadge]][ruff] [![emailbadge]][email]

[update]: https://github.com/eduardotlc/zot2sioyek/commits/master/
[updatebadge]: https://img.shields.io/badge/Updated-August_2024-93ddfb?style=for-the-badge&logo=googlecalendar
[license]: https://opensource.org/licenses/mit
[pypi]: https://pypi.org/project/zot2sioyek/
[ruff]: https://github.com/astral-sh/ruff
[pypibadge]: https://img.shields.io/pypi/v/zot2sioyek.svg?logo=python&logoColor=yellow&color=7e7edd&style=for-the-badge
[email]: mailto:eduardotcampos@usp.br
[emailbadge]: https://img.shields.io/badge/Email-7e7edd?style=for-the-badge&logo=gmail
[mitbadge]: https://img.shields.io/badge/License-MIT-9aefea?style=for-the-badge&logo=gitbook
[ruffbadge]: https://img.shields.io/badge/Ruff-4a4a4a?style=for-the-badge&logo=ruff

## 📖 Contents

- ✨ [Features](#-features)
- 📚 [Requirements](#-requirements)
  - 🐍 [Conda](#-conda)
- 📦 [Installation](#-installation)
- 🔧 [Configuration](#-configuration)
  - 🎨 [Colors](#-colors)
- 💻 [Client](#-client)
- 📝 [TODO](#-todo)
- 🤝 [Contributing](#-contributing)
- 💓 [Aknowledgements](#-aknowledgements)

## ✨ Features

- Embed zotero highlights to the sioyek database:

```bash
python zot2sioyek.py --insert-highlights "/path/to/file.pdf"
```

- Print in terminal the text of all the highlights from a zotero file, colored with the highlight
  color

```bash
python zot2sioyek.py --print-annotation-text "/path/to/file.pdf"
```

- To see all available commands:

```bash
python zot2sioyek.py --help
```

> [!NOTE]
> If installed through pip, you can run only `zot2sioyek` instead of `python zot2sioyek.py`.

## 📚 Requirements

Requirements are automatic installed when this script is installed with pip

- pyzotero

- pymupdf

- PyQt5

- regex

- sqlite3

```bash
python -m pip install pyzotero pymupdf PyQt5 regex sqlite3
```

### 🐍 Conda

If wanted, requirements may be installed with conda, to run this script in a conda environment.

Inside this repo, run:

```bash
conda env create --file env.yml
```

## 📦 Installation

To run the script without installation, simply clone the repo or download /src/zot2sioyek/zot2sioyek.py
and run it directly.

Default installation is done by

```bash
python -m pip install zot2sioyek
```

Being possible after install to run the comman with `zot2sioyek` in terminal.

Other possible approach to install is cloning the repo and installing locally

```bash
git clone https://github.com/eduardotlc/zot2sioyek
cd zot2sioyek
python -m pip install -e .
```

## 🔧 Configuration

To use this script define the variables in zot2sioyek.py:

- `SIOYEK_PATH`: Sioyek binary path.

- `SIOYEK_LOCAL_DATABASE_FILE_PATH`: Sioyek .db local database file path.

- `SIOYEK_SHARED_DATABASE_FILE_PATH`: Sioyek .db shared database file path.

- `ZOTERO_LIBRARY_ID`: Your personal library ID available [Here](https://www.zotero.org/settings/keys),
  in the section Your userID for use in API calls.

- `ZOTERO_API_KEY`: Api key, you can obtain [Here](https://www.zotero.org/settings/keys/new).

- `ZOTERO_LIBRARY_TYPE`: Zotero library type, can be `'user'` or `'group'`.

- `ZOTERO_LOCAL_DIR`: Zotero local storage folder, like `/home/user/Zotero/storage`.

- `ZOTERO_TO_SIOYEK_COLORS`: Sioyek highlight type letter associated to each zotero highlight color
  (Optional).

> [!NOTE]
> The variables can also be defined as envrinoment variables (at your .zshrc/.bashrc etc...), with
> the exact same names as the script variables above, and ZOTERO_TO_SIOYEK_COLORS if defined should
> be defined as a string like:
> export ZOTERO_TO_SIOYEK_COLORS='{ "#5fb236": "h", "#a28ae5": "i", "#e56eee": "i", "#2ea8e5": "d", "#ff6666": "e", "#f19837": "r", "#ffd400": "s"}'

### 🎨 Colors

- This script defines `ZOTERO_TO_SIOYEK_COLORS` variable based on the most close colors of default
  sioyek config, to the zotero highlight colors. The conversion looks like the following (Zotero
  colors in the upper row, sioyek colors in the lower row):

![comparison colors](/images/coparison_colors.png)

- If you want to have the exact same colors of zotero highlights in sioyek, add the following to
  your sioyek `prefs_user.config`:

```
highlight_color_g 0.37 0.70 0.21
highlight_color_a 0.63 0.54 0.90
highlight_color_p 0.90 0.43 0.93
highlight_color_b 0.18 0.66 0.90
highlight_color_r 1.00 0.40 0.40
highlight_color_o 0.95 0.60 0.22
highlight_color_y 1.00 0.83 0.00
```

- Or to any highlight letter you want, since the defined letter on `prefs_user.config` and the script
  variable `ZOTERO_TO_SIOYEK_COLORS` match.

## 💻 Client

**The following commands are available through:**

In a local folder after downloading the script, cd in `/src/zot2sioyek` and run

> python zot2sioyek.py [FLAG] [ARGS]

If installed through pip or through `cloning` or with `pip install -e .` in the repo root, the 2
following commands are available

> python -m zot2sioyek.zot2sioyek [FLAG] [ARGS]

> zot2sioyek [FLAG] [ARGS]

```bash
FLAGS                              ARGUMENTS
=====                              ==========


Script general utils.
----------------------

-h, --help
Print this script help.

Zotero Managing Commands.
--------------------------

-g, --get-highlights               [file_name_or_path]
Print all highlights from a given zotero file.
-p, --print-annotation-text        [file_name_or_path]
print all highlighted text for a given zotero PDF local file.
-T, --zotero-tags                  [file_name_or_path]
Prints a zotero PDF attachment parent item existing arguments.
-A, --add-zotero-tag               [file_name_or_path], [tag_str_to_add]
Add a tag to a zotero PDF attachment parent item. Takes arguments file name or
path, and tag str to add.
-R, --remove-zotero-tag            [file_name_or_path], [tag_str_to_remove]
Remove a tag from a zotero PDF attachment parent item. Takes arguments file name or
path, and tag str to remove.

Sioyek Main Commands.
----------------------

-f, --list-sioyek-files
Print all files in sioyek local database
-H, --list-sioyek-hash             [file_name_or_path]
print a sioyek database pdf file md5sum hash.
-l, --print-sioyek-attributes      [file_name_or_path]
Print all Attributes and values in a sioyek database PDF file.
-i, --insert-highlight             [file_name_or_path]
Insert highlights in a sioyek database PDF file, importing this highlights from this
PDF file zotero attachment highlight.
-S, --list-all-sioyek-highlights
Print all sioyek highlights

If an argument passed after a flag contain blank spaces, remember to quote wrap it,
while not being necessary case inputted after through prompted option.

Author: eduardotcampos@usp.br
```

## 📝 TODO

- Embed all zotero database highlights starting from a specified date.

- Create import from sioyek database to zotero database highlights.

  - Currently, I couldn't find a way of adding zotero highlights through pyzotero, or through
    zotero api/sql. If anyone knows how to do it, please message or email me so that I can update
    this script, or feel free to implement the needed updates and send a pull request, I'll be
    very thankful.

## 🤝 Contributing

Feel free to make [pending](#-todo) or other optimizations and pull requests, this script is
still under development and any contribution is very much appreciated.

- Clone the repo to your local environment:

## 💓 Aknowledgements

- [Ahrm](https://github.com/ahrm) for developing [Sioyek](https://github.com/ahrm/sioyek) PDF reader.

- [Urschrei](https://github.com/urschrei) for [Pyzotero](https://github.com/urschrei/pyzotero)

- [Blob42](https://github.com/blob42) for [Koreader-sioyek-import](https://github.com/blob42/koreader-sioyek-import),
  which parts of this script was based from.

- The [Zotero](https://www.zotero.org/) team.
