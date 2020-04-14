#!/usr/bin/env python3
import re 
import codecs 
import typing as t
import json 

KEY_RX = re.compile(
    r'\\entry{(?P<key>[^}]*)}'
)

def extract_bibkeys(bbl_file: str) -> t.List[str]:
    """extract all bib entry keys from a bbl file"""
    with codecs.open(bbl_file, 'r', 'utf-8') as bf:
        bbl_str = bf.read() 
        print(bbl_str)
        z = KEY_RX.findall(bbl_str)
        if z:
            with codecs.open('used_bib_entries.json', 'w', 'utf-8') as jf:
                json.dump({
                    'used_bib_entries': z
                }, jf, indent=4)
            


if __name__ == '__main__':
    extract_bibkeys('LONG-GONG-DISSERTATION-2020.bbl')