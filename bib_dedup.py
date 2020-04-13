# !/usr/bin/env python3
from __future__ import absolute_import
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import convert_to_unicode
from bibtexparser.customization import homogenize_latex_encoding
import editdistance
import codecs
import click
import typing as t
import os
import os.path
import logging
import json


DEFAULT_LOG_FILE = "example.log"


def setup_logger(log_file: str = DEFAULT_LOG_FILE, level: t.Optional[int] = None):
    """Configure a custom logger"""
    # create logger with 'spam_application'
    logger = logging.getLogger()
    root_log_level = level if (level is not None) else logging.DEBUG
    logger.setLevel(root_log_level)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(root_log_level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


def get_bibfiles(folder: str) -> t.List[str]:
    """All all bib files within the folder `folder`"""
    full_pathname = os.path.normpath(os.path.abspath(folder))
    bib_files = []
    for f in os.listdir(full_pathname):
        fullname = os.path.join(full_pathname, f)
        if f.endswith(".bib") and os.path.isfile(fullname):
            logging.debug(f'get bibfile "{f}" from directory "{full_pathname}"')
            bib_files.append(fullname)
    return bib_files


def parse_bib_database(bibFile: str) -> BibDatabase:
    """Parse bib file `bibFile`"""
    logging.debug(f'reading bibfile "{bibFile}"')
    with codecs.open(bibFile, "r", "utf-8") as bibtex_file:
        parser = BibTexParser(common_strings=True, interpolate_strings=False)
        # parser.customization = convert_to_unicode
        try:
            return bibtexparser.loads(bibtex_file.read(), parser=parser)
        except IndexError as e:
            logging.error(f"{e}")
        except Exception as e:
            logging.error(f"{e}")
        return BibDatabase()


def bib_unique(
    entries: t.List[t.Dict],
) -> t.Tuple[t.List[t.Dict], t.List[t.Dict], t.Dict[str, t.List[str]]]:
    """Remove duplicated entries"""
    unique_ids = []
    duplicated_ids = {}
    THRESHOLD = 0.1
    n_entries = len(entries)
    dup_set = set({})
    for i in range(n_entries):
        if i in dup_set:
            continue
        dup_for_this = [i]
        for j in range(n_entries):
            ea = entries[i]
            eb = entries[j]
            if j != i and ea["ENTRYTYPE"].lower() == eb["ENTRYTYPE"].lower():
                if ea["ID"] == eb["ID"]:
                    # we always consider entries with the same IDs as duplication
                    # although usually they won't cause any problem
                    dup_for_this.append(j)
                else:
                    # for entries with different IDs, we compare the editting
                    # distance between their titles, if the result is equal to
                    # or less than a threshold, we consider them as duplications
                    # for a single entry.
                    ta = ea.get("title", "").lower().strip(' \n\r}{"')
                    tb = eb.get("title", "").lower().strip(' \n\r}{"')
                    l = max(len(ta), len(tb))
                    if editdistance.eval(ta, tb) <= l * THRESHOLD:
                        dup_for_this.append(j)
        if len(dup_for_this) > 1:
            duplicated_ids[entries[dup_for_this[0]]["ID"]] = [
                entries[k]["ID"] for k in dup_for_this[1:]
            ]
            for e in dup_for_this:
                dup_set.add(e)
        unique_ids.append(i)
    unique_entries = [entries[i] for i in unique_ids]
    duplicated_entries = [entries[i] for i in dup_set]
    return unique_entries, duplicated_entries, duplicated_ids


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-d", "--directory", type=str, help="Directory for storing bibtex files")
def bib_dedup(directory):
    """Detect and remove duplicated bib entries"""
    entries = []
    for bib_file in get_bibfiles(directory):
        db = parse_bib_database(bib_file)
        entries.extend(db.entries)
    raw_db = BibDatabase()
    raw_db.entries = entries
    writer = BibTexWriter()
    with codecs.open("merged_raw.bib", "w", "utf-8") as bibfile:
        bibfile.write(writer.write(raw_db))
    unique_entries, dup_entries, dup_maps = bib_unique(entries)
    uni_db = BibDatabase()
    uni_db.entries = unique_entries
    dup_db = BibDatabase()
    dup_db.entries = dup_entries
    with codecs.open("merged_unique.bib", "w", "utf-8") as u_bibfile, codecs.open(
        "merged_dup.bib", "w", "utf-8"
    ) as d_bibfile:
        u_bibfile.write(writer.write(uni_db))
        d_bibfile.write(writer.write(dup_db))
    with codecs.open("dup-maps.json", "w", "utf-8") as jf:
        json.dump(dup_maps, jf, indent=4)


if __name__ == "__main__":
    setup_logger()
    bib_dedup()
