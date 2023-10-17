import glob
from acdh_tei_pyutils.tei import TeiReader
import lxml.etree as ET

files_44_9 = glob.glob("./data/work-in-progress/44_9/**/*.xml", recursive=True)
files_44_10 = glob.glob("./data/work-in-progress/44_10/**/*.xml", recursive=True)
files = sorted(files_44_9 + files_44_10)

for file_path in files:
    try:
        doc = TeiReader(file_path)
    except Exception as e:
        print(f"Bad XML: {file_path}")
        continue
    for pb in doc.any_xpath(".//tei:pb"):
        n = pb.attrib["n"]
        try:
            ed = pb.attrib["ed"]
        except KeyError:
            continue
        pb.attrib["n"] = ed
        pb.attrib["ed"] = n
    doc.tree_to_file(file_path)
