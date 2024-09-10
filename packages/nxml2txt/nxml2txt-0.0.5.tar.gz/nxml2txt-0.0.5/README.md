nxml2txt
========

NLM .nxml to text format conversion 

Usage:

    ./nxml2txt NXMLFILE [TEXTFILE] [SOFILE]

For example (using test document):

    ./nxml2txt test/PMC3357053.nxml test/PMC3357053.txt test/PMC3357053.so

This creates the files `test/PMC3357053.txt`, containing the text
content of the input document, and `test/PMC3357053.so`, containing
the annotations (XML elements and their attributes) in a simple
standoff format.

nxml2txt assumes a unix-like environment.
If the input .nxml file contains embedded TeX-math, nxml2txt
requires [LaTeX](http://en.wikipedia.org/wiki/LaTeX) and
[catdvi](http://catdvi.sourceforge.net/).

This tool was originally introduced as part of the BioNLP Shared Task
2011 supporting resources
(https://github.com/ninjin/bionlp_st_2011_supporting).
