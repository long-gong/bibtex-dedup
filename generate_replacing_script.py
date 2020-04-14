#!/usr/bin/env python3
import codecs
import json
HDR="""#!/usr/bin/env bash
set -e
tex_files=$(find ./ -type f | grep -E '\.tex')

for f in tex_files
do
    echo "Processing ${f} ..."
"""

if __name__ == "__main__":
    with codecs.open('sub-dup-maps.json', 'r', 'utf-8') as jf:
        dup_maps = json.load(jf, encoding='utf-8')
    lines = []
    for key,value in dup_maps.items():
        for val in value:
            lines.append(
                f"\techo \"sed -i 's/{val}/{key}/g' $f\""
            )
            lines.append(
                f"\tsed -i 's/{val}/{key}/g' $f"
            )
    lines.append('done')
    with open('replace_all_duplicated_bibkeys.sh', 'w') as bf:
        bf.write(HDR)
        bf.write('\n'.join(lines))


