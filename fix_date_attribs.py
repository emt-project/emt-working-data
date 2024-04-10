import glob
from acdh_tei_pyutils.tei import TeiReader

files = glob.glob("./data/**/*.xml", recursive=True)


for x in files:
    doc = TeiReader(x)
    for d in doc.any_xpath(".//tei:correspAction//tei:date[@when]"):
        d.attrib["when-iso"] = d.attrib.pop("when")
    doc.tree_to_file(x)
