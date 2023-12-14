import glob
from acdh_tei_pyutils.tei import TeiReader

files = sorted(glob.glob("./data/work-in-progress/*/*.xml", recursive=True))
replace_patterns = [
    ['<title type="main">nan,', '<title type="main">unbekannte(r) AbsenderIn,'],
    ['<persName ref="#">nan</persName>', '<persName>unbekannt</persName>'],
    ['nan am nan', 'ohne Ort und ohne Datum'],
    # ['<placeName ref="#"/>', '<placeName>unbkeannt</placeName>'],
    ['<author>nan</author>', '']
]

broken = []
modified = set()
for x in files:
    try:
        doc = TeiReader(x)
    except Exception as e:
        broken.append([x, e])
        continue
    text = doc.return_string()
    save = False
    for p in replace_patterns:
        if p[0] in text:
            save = True
            modified.add(x)
            text = text.replace(p[0], p[1])
    if save:
        doc = TeiReader(text)
        doc.tree_to_file(x)