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
from titlecase import titlecase


DEFAULT_LOG_FILE = "example.log"


class BibEntryCustomization:
    @staticmethod
    def _remove_bracket(e_title: str) -> str:
        """remove unnecessary '{' and '}'"""
        stack = []
        if e_title[0] == "{" and e_title[-1] == "}":
            for i, ch in enumerate(e_title):
                if ch == "{" and (i == 0 or (i > 0 and e_title[i - 1] != "//")):
                    stack.append((i, ch))
                elif ch == "}" and e_title[i - 1] != "//":
                    index, ch = stack.pop()
                    if index == 0:
                        if i == len(e_title) - 1:
                            return e_title[1:-1]
                        break
        return e_title

    @staticmethod
    def title_strip(e_title: str) -> str:
        """title strip"""
        return BibEntryCustomization._remove_bracket(e_title.strip(" \n\r"))

    @staticmethod
    def title_capitalization(e_title: str) -> str:
        """title capitalization"""
        dollars_left = []
        dollars_right = []
        cnt = 1
        for k in range(len(e_title)):
            if e_title[k] == "$" and (k == 0 or (k > 0 and e_title[k - 1] != "//")):
                if cnt % 2 == 1:
                    dollars_left.append(k)
                else:
                    dollars_right.append(k)
                cnt += 1
        if len(dollars_left) != len(dollars_right):
            raise RuntimeError('Unknown error regarding "$"')
        substr_raw = []
        substr_rep = []
        for l, r in zip(dollars_left, dollars_right):
            raw = e_title[l : (r + 1)]
            substr_raw.append(raw)
            substr_rep.append("{" + raw + "}")
        for raw, rep in zip(substr_raw, substr_rep):
            e_title = e_title.replace(raw, rep, 1)

        return titlecase(e_title)

    @staticmethod
    def title_all(e_title: str) -> str:
        """apply all customizations to title"""
        title_customizations = [
            BibEntryCustomization.title_strip,
            BibEntryCustomization.title_capitalization,
        ]
        for f in title_customizations:
            e_title = f(e_title)
        return e_title

    @staticmethod
    def journal_booktitle_unify(entries: t.List[t.Dict]) -> t.List[t.Dict[str, str]]:
        """unify the formating for the titles of both journals and conferences (using full name)"""

        def _process(
            entries: t.List[t.Dict], etype: str, val: str, replacing_guide_file: str
        ) -> t.List[t.Dict[str, str]]:
            rep_rules = {}
            with codecs.open(replacing_guide_file, "r", "utf-8") as gf:
                for line in gf:
                    line = line.strip()
                    raw, sep, rep = line.partition("=")
                    logging.debug(f'{line}')
                    if len(sep) != 0:
                        rep_rules[raw] = rep
            logging.debug(f'{rep_rules}')
            for e in entries:
                if e["ENTRYTYPE"].lower() == etype.lower():
                    value = e.get(val, "")
                    if value in rep_rules:
                        logging.debug("Before: %s", e[val])
                        e[val] = rep_rules[value]
                        logging.debug("After: %s", e[val])
            return entries

        entries = _process(entries, "InProceedings", "booktitle", "conferences.txt")
        return _process(entries, "Article", "journal", "journals.txt")


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
            this_id = entries[dup_for_this[0]]["ID"]
            other_ids = set([entries[k]["ID"] for k in dup_for_this])
            other_ids.remove(this_id)
            if len(other_ids) != 0:
                duplicated_ids[this_id] = list(other_ids)
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

    # book_titles = set({e.get('booktitle', '') for e in unique_entries})
    # journals = set({e.get('journal', '') for e in unique_entries})
    # with codecs.open('conferences.txt', 'w', 'utf-8') as cf:
    #     cf.write('\n'.join(book_titles))
    # with codecs.open('journals.txt', 'w', 'utf-8') as jf:
    #     jf.write('\n'.join(journals))

    for e in unique_entries:
        if "title" in e:
            logging.debug("Before: %s", e["title"])
            e["title"] = BibEntryCustomization.title_all(e["title"])
            logging.debug("After: %s", e["title"])

    logging.debug('Processing book titles and journal names ...')
    unique_entries = BibEntryCustomization.journal_booktitle_unify(unique_entries)
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
    with codecs.open('used_bib_entries.json', 'r', 'utf-8') as uf:
        used_ids = set(json.load(uf, encoding='utf-8').get('used_bib_entries', []))
    used_entries = [e for e in unique_entries if e['ID'] in used_ids]
    used_db = BibDatabase()
    used_db.entries = used_entries
    with codecs.open("used.bib", "w", "utf-8") as u_bibfile:
        u_bibfile.write(writer.write(used_db))




if __name__ == "__main__":
    setup_logger()
    bib_dedup()
