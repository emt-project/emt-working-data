import glob
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader


print("adds missing '#' to tei:rs @ref")
files = sorted(glob.glob("./data/work-in-progress/*/*.xml", recursive=True))

fixed_values = 0
good_values = 0
all_refs = 0
for x in tqdm(files):
    try:
        doc = TeiReader(x)
    except Exception as e:
        print(x, e)
        continue
    for rs in doc.any_xpath(".//tei:body//tei:rs[@ref]"):
        all_refs += 1
        ref = rs.attrib["ref"]
        if ref == "#":
            rs.pop("ref")
            fixed_values += 1
        elif ref[0] != '#':
            rs.attrib["ref"] = f"#{ref}"
            fixed_values += 1
        else:
            good_values += 1
    doc.tree_to_file(x)

print(f"fixed {fixed_values} out of {all_refs} refs")
