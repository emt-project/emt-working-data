import glob
from acdh_tei_pyutils.tei import TeiReader

files = sorted(glob.glob("./data/**/*.xml", recursive=True))
print(len(files))

for x in files:
    doc = TeiReader(x)
    save = False
    for y in doc.any_xpath(".//tei:zone[@points]"):
        points = y.attrib["points"].split(" ")
        if len(points) < 3:
            del y.attrib["points"]
            save = True
    for y in doc.any_xpath(".//tei:zone[@subtype]"):
        if y.attrib["subtype"]:
            pass
        else:
            del y.attrib["subtype"]
            save = True
    if save:
        doc.tree_to_file(x)
