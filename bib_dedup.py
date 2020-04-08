#!/usr/bin/env python3
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import convert_to_unicode
import editdistance
import click
import typing as t
import os
import os.path


def getBibfiles(folder: str) -> t.List[str]:
    """All all bib files within the folder `folder`"""
    full_pathname = os.path.normpath(os.path.abspath(folder))
    bib_files = []
    for f in os.listdir(full_pathname):
        if os.path.isfile(f) and f.endswith(".bib"):
            bib_files.append(os.path.join(full_pathname, f))
    return bib_files


def parseBibDatabase(bibFile: str) -> BibDatabase:
    """Parse bib file `bibFile`"""
    with open(bibFile, 'w') as bibtex_file:
        parser = BibTexParser(common_strings=False)
        parser.customization = convert_to_unicode
        return bibtexparser.loads(bibtex_file.read(), parser=parser)

