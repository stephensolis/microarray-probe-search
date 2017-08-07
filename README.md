# microarray-probe-search

[![Build Status](https://travis-ci.org/stephensolis/microarray-probe-search.svg?branch=master)](https://travis-ci.org/stephensolis/microarray-probe-search)

This is a simple script for searching for exact matches of DNA microarray probe sequences in a genome.

The defaults are set up for Affymetrix `probe_tab` files, but you can easily use any tsv file by setting the `--probe-sequence-header` and `--probe-id-header` parameters.

It's not particularly efficient, but can search 2.5 million probes in a 2.6Gbp genome in ~20 minutes.

Since this is intended to run on the built-in Python on macOS, there are no external dependencies. Python 2.7+, 3.3+, and PyPy will work.

## Detailed instructions (for a Mac)

1. [Right-click here](https://raw.githubusercontent.com/stephensolis/microarray-probe-search/master/sequence-search.py) and select 'Save as', and save the file somewhere.
2. Download the fasta files for whichever genome you want and put them all in a new folder.
3. Open Terminal (in Applications -> Utilities).
4. Type 'python' (without the quotes) and press space.
5. Drag and drop the sequence-search.py file to the Terminal window (some text will appear) and press space.
6. Type the length of the probes you want (eg. 25) and press space.
7. Drag and drop the probes file you want to use to the Terminal window and press space.
8. Drag and drop the folder with genome sequences to the Terminal window.
9. Press enter and wait about 20 minutes.

## Usage

    usage: sequence-search.py [-h] [--probe-sequence-header PROBE_SEQUENCE_HEADER]
                              [--probe-id-header PROBE_ID_HEADER]
                              probe_length probe_sequence_file genome_directory

    Search for microarray probe sequences in a genome.

    positional arguments:
      probe_length          the length of the probe sequences to search for
      probe_sequence_file   the TSV file of probe sequences
      genome_directory      the directory containing the genome in FASTA files

    optional arguments:
      -h, --help            show this help message and exit
      --probe-sequence-header PROBE_SEQUENCE_HEADER
                            the name of the column of probe_sequence_file
                            containing probe sequences
      --probe-id-header PROBE_ID_HEADER
                            the name of the column of probe_sequence_file
                            containing probe IDs

## License ![License](http://img.shields.io/:license-mit-blue.svg)

    The MIT License (MIT)

    Copyright (c) 2017 Stephen

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
