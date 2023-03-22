import glob
import os
import pandas as pd
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader


METS_DIR = "/home/csae8092/repos/emt/emt-transkribus-export/mets"
files = sorted(glob.glob('./data/work-in-progress/*/*.xml'))

nsmap = {
    "mets": "http://www.loc.gov/METS/",
    "xlink": "http://www.w3.org/1999/xlink"
}

fails = []
trouble_makers = []
for x in tqdm(files, total=len(files)):
    try:
        doc = TeiReader(x)
    except:
        fails.append({"mets_path": x, "error": "not well formed file"})
        continue
    # print(x)
    transkribus_doc_id = doc.any_xpath('.//tei:idno[@type="transkribus-doc-id"]/text()')[0]
    transkribus_col_id = doc.any_xpath('.//tei:idno[@type="transkribus-col-id"]/text()')[0]
    mets_path = os.path.join(METS_DIR, transkribus_col_id, f"{transkribus_doc_id}_mets.xml")
    # print(mets_path)
    try:
        mets_doc = TeiReader(mets_path)
    except Exception as e:
        fails.append(
            {"mets_path": mets_path, "error": e}
        )
        continue
    images = []
    for y in mets_doc.tree.xpath('.//mets:fileGrp[@ID="IMG"]//mets:file/mets:FLocat/@xlink:href', namespaces=nsmap):
        images.append(y)
    tei_pbs = doc.any_xpath('.//tei:pb')
    if len(tei_pbs) != len(images):
        trouble_makers.append((x, mets_path))
    else:
        for i, p in enumerate(tei_pbs):
            p.attrib["source"] = images[i]
        doc.tree_to_file(x)
    
df = pd.DataFrame(fails)
df.to_csv("error_log.csv", index=False)

for x in tqdm(trouble_makers, total=len(trouble_makers)):
    doc = TeiReader(x[0])
    file_list_name = x[1].replace("_mets.xml", "_image_name.xml")
    file_list = TeiReader(file_list_name)
    mets = TeiReader(x[1])
    tei_pbs = doc.any_xpath('.//tei:pb')
    file_list_dict = {}
    facs_list = mets.tree.xpath('.//mets:fileGrp[@ID="IMG"]//mets:file/mets:FLocat/@xlink:href', namespaces=nsmap)
    for item in file_list.any_xpath('.//item'):
        file_list_dict[item.text] = item.attrib["n"]
    for p in tei_pbs:
        img_name = p.attrib["{http://www.w3.org/XML/1998/namespace}id"]
        img_index = file_list_dict[img_name]
        try:
            facs_url = facs_list[int(img_index)]
        except IndexError:
            print(img_index, x)
            continue
        p.attrib["source"] = facs_url
    doc.tree_to_file(x[0])
        
