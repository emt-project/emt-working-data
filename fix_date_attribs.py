import glob
import re
from acdh_tei_pyutils.tei import TeiReader

files = glob.glob("./data/**/*.xml", recursive=True)

for x in files:
    doc = TeiReader(x)
    for d in doc.any_xpath(".//tei:correspAction//tei:date[@when]"):
        d.attrib["when-iso"] = d.attrib.pop("when")

    for d in doc.any_xpath(".//tei:body//tei:date[@when]"):
        date_value = d.attrib["when"]
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_value):
            continue
        else:
            d.attrib["when-iso"] = d.attrib.pop("when")
    doc.tree_to_file(x)
