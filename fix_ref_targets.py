import glob
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader

files = sorted(glob.glob("./data/work-in-progress/*/*.xml", recursive=True))

items = set()
for x in tqdm(files):
    try:
        doc = TeiReader(x)
    except:  # noqa:
        continue
    for y in doc.any_xpath(".//tei:ref[@target]"):
        target = y.attrib["target"]
        target = target.split("/")[-1]
        target = target.split(".")[0]
        target = target.split("#")[-1]
        target = target.lower()
        target = f"#{target}.xml"
        y.attrib["target"] = target
    doc.tree_to_file(x)
