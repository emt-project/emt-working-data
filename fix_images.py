import glob
import os
import pandas as pd
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader


METS_DIR = "/home/csae8092/repos/emt/emt-transkribus-export/mets"
files = sorted(glob.glob('./data/work-in-progress/*/*.xml'))

fails = []
for x in tqdm(files, total=len(files)):
    doc = TeiReader(x)
    transkribus_doc_id = doc.any_xpath('.//tei:idno[@type="transkribus-doc-id"]/text()')[0]
    transkribus_col_id = doc.any_xpath('.//tei:idno[@type="transkribus-col-id"]/text()')[0]
    mets_path = os.path.join(METS_DIR, transkribus_col_id, f"{transkribus_doc_id}_mets.xml")
    try:
        mets_doc = TeiReader(mets_path)
    except Exception as e:
        fails.append(
            {"mets_path": mets_path, "error": e}
        )
df = pd.DataFrame(fails)
df.to_csv("error_log.csv", index=False)
print(transkribus_col_id, transkribus_doc_id, mets_path)
# mets/58705/565905_mets.xml
