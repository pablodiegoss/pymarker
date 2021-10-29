# PyMarker

A python package to generate AR markers and patterns based on input images.

## Installation

PyMarker is available through pip and [Pypi](https://pypi.org/project/pymarker/).

```bash
python3 -m pip install pymarker --user
// or
pip3 install pymarker --user
```

## Usage

Pymarker provides two features for a marker-based AR, generating Pattern files (.patt) and Markers (.png). The marker will be used by the user to visualize some augmented reality, the pattern file for the system to be able to recognize the marker.

An example input image:
![Example of an input image](images/hiro.jpg)

Expected output patt:
![Example output for pattern file](images/patt_example.png)

Expected output marker:
![Example of a generated marker](images/marker_example.png)

### Commands

By default pymarker receives an image and generate both patt and marker

```bash
$ pymarker tests/input/hiro.jpg
```

However, if needed the flag `-p` or `--patt` can gerate only the patt file for the input:

```bash
$ pymarker -p tests/input/hiro.jpg
// or
$ pymarker --patt tests/input/hiro.jpg
```

The same can happen for markers using the `-m` or `--marker` which generates only the marker:

```bash
$ pymarker -m tests/input/hiro.jpg
// or
$ pymarker --marker tests/input/hiro.jpg
```

The marker border size can be adjusted with `-b`, the default value being 50%.

```bash
$ pymarker -b 40 tests/input/hiro.jpg
```

### Modules

You can use the functions directly from your python code to generate markers and patts.

```
from pymarker.core import generate_patt, generate_marker

def main():
    filename = "tests/input/hiro.jpg"
    border_size = 50 // size in percentage

    generate_patt(filename)
    generate_marker(filename,border_size)

```
