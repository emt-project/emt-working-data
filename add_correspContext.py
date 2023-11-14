import glob
from acdh_tei_pyutils.tei import TeiReader
import lxml.etree as ET
import pandas as pd

files = sorted(glob.glob("./data/work-in-progress/**/*.xml", recursive=True))
empress_id = "#emt_person_id__9"

non_dateable = [] # TODO: gets populated, but unused as per now
broken = [] # TODO: gets populated, but unused as per now
items = []
thread_ids = set()
for x in files:
    try:
        doc = TeiReader(x)
    except Exception as e:
        broken.append([e, x])
        continue
    try:
        date = doc.any_xpath(".//tei:correspAction[@type='sent']/tei:date/@when-iso")[0]
    except IndexError:
        date = "1000-01-01"
        non_dateable.append(x)
    corresp_id = "_".join(sorted([x for x in doc.any_xpath(".//tei:correspAction/tei:persName/@ref") if x != empress_id]))
    corresp_names = " und ".join([(x.xpath('./text()')[0] if len(x.xpath('./text()')) > 0 else '?') for x in doc.any_xpath(".//tei:correspAction/tei:persName") if x.xpath('./@ref')[0] != empress_id])
    item = {
        "id": x,
        "corresp_id": corresp_id,
        "corresp_names": corresp_names,
        "date": date,
        "title": doc.any_xpath(".//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title/text()")[0]
    }
    items.append(item)
    thread_ids.add(item["corresp_id"])

df = pd.DataFrame(items)

for i, ndf in df.groupby("corresp_id"):
    sorted_df = ndf.sort_values("date")
    sorted_df["prev"] = sorted_df["id"].shift(-1)
    sorted_df["next"] = sorted_df["id"].shift(1)
    sorted_df["prev_title"] = sorted_df["title"].shift(-1)
    sorted_df["next_title"] = sorted_df["title"].shift(1)
    for j, x in sorted_df.iterrows():
        try:
            doc = TeiReader(x["id"])
        except Exception:
            print(f"Cannot add correspContext to file: {x['id']}")
            continue

        for existing_corresp_context in doc.any_xpath("//tei:correspContext"):
            existing_corresp_context.getparent().remove(existing_corresp_context)

        correspDesc = doc.any_xpath("//tei:correspDesc")[0]
        correspContext = ET.SubElement(correspDesc, 'correspContext')
        ref = ET.SubElement(correspContext, 'ref', type="belongsToCorrespondence", target=x["corresp_id"])
        ref.text = "Korrespondenz mit " + x["corresp_names"]
        prevCorr = ET.SubElement(correspContext, 'ref', subtype="previous_letter", type="withinCorrespondence", source=x["corresp_id"], target="" if x["prev"] is None else x["prev"].split('/')[-1])
        prevCorr.text = "" if x["prev_title"] is None else x["prev_title"].split('/')[-1]
        nextCorr = ET.SubElement(correspContext, 'ref', subtype="next_letter", type="withinCorrespondence", source=x["corresp_id"], target="" if x["next"] is None else x["next"].split('/')[-1])
        nextCorr.text = "" if x["next_title"] is None else x["next_title"].split('/')[-1]
        doc.tree_to_file(x["id"])
