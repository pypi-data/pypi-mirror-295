<h1 align="center">
TidySorter
</h1>
<p align="center">
Effortlessly organize your files into neatly categorized folders, making it easier to prepare for system formatting or reinstallation, or simply to clean up cluttered directories filled with accumulated files.
</p>
<p align="center">
Compatible with macOS, Linux, and Windows.
</p>

## Installation

**Install using `pip`**: Simply run:
```console
$ pip install --user tidysorter
```

## Usage

Once installed, you can use TidySorter directly from the command line. To get a list of available options and usage instructions, run:
```console
$ tidysorter --help
usage: tidysorter.py [-h] [-f FOLDER] [-q] [-R] [-s] [-S] [-v] [source_folder]

positional arguments:
  source_folder         The source folder to sort

options:
  -h, --help            show this help message and exit
  -f  --folder          Custom name of the master folder
  -q  --quiet           Suppress all console output (quiet mode)
  -R  --recursive       Apply sorting recursively to subfolders
  -s, --simulate        Enable simulation mode (no changes will be made)
  -S, --safe            Prevent deletion of empty folders and shortcut files. By default, empty folders and shortcut files will be removed during sorting.
  -v, --version         Display the version number
```