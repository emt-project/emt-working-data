import glob
from acdh_tei_pyutils.tei import TeiReader
import lxml.etree as ET

files = [
    "./data/work-in-progress/44_10/kasten_blau_44_10_0020.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0031.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0034.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0058.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0077.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0094.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0108.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0108.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0108.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0126.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0129.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0135.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0142.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0147.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0155.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0161.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0191.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0194.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0230.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0245.xml",
    "./data/work-in-progress/44_10/kasten_blau_44_10_0257.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0014.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0086.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0098.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0149.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0171.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0171.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0219.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0231.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0246.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0250.xml",
    "./data/work-in-progress/44_9/kasten_blau_44_9_0258.xml",
]

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
            print(f"Missing ed in: {file_path}")
            continue
        pb.attrib["n"] = ed
        pb.attrib["ed"] = n
    doc.tree_to_file(file_path)
