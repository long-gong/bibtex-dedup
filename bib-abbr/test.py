#!/usr/bin/env python3
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
import codecs
import json 

if __name__ == "__main__":
    with codecs.open('NTGabrv.bib', 'r', 'utf-8') as bf:
        bib_database = bibtexparser.load(bf)
    print(bib_database.strings)
    with codecs.open('test.json', 'w', 'utf-8') as jf:
        json.dump(bib_database.strings, jf, indent=4)
