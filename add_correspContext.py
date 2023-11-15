import glob
from acdh_tei_pyutils.tei import TeiReader
import lxml.etree as ET
import pandas as pd
from tqdm import tqdm

files = sorted(glob.glob("./data/work-in-progress/**/*.xml", recursive=True))
empress_id = "#emt_person_id__9"

non_dateable = [] # TODO: gets populated, but unused as per now
broken = [] # TODO: gets populated, but unused as per now
items = []
thread_ids = set()
date_marker = '1677-01-01' # Extreme lower boundary of dates. This variable is used for storing the "previous date" to date undated letters
print(f"fetching data from {len(files)} files")
for x in tqdm(files, total=len(files)):
    try:
        doc = TeiReader(x)
    except Exception as e:
        broken.append([e, x])
        continue

    dateAttribs = doc.any_xpath(".//tei:correspAction[@type='sent']/tei:date/@when-iso")
    if (len(dateAttribs) > 0):
        date = dateAttribs[0]
    else:
        dateAttribs = date = doc.any_xpath(".//tei:correspAction[@type='sent']/tei:date/@notBefore")
        if (len(dateAttribs) > 0):
            date = dateAttribs[0]
        else:
            date = date_marker
            non_dateable.append(x)
    date_marker = date

    corresp_id = "_".join(sorted([x for x in doc.any_xpath(".//tei:correspAction/tei:persName/@ref") if x != empress_id]))
    corresp_names = " und ".join([(x.text if x.text is not None else '?') for x in doc.any_xpath(".//tei:correspAction/tei:persName") if x.attrib['ref'] != empress_id])
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
df = df.sort_values("date")
df["gen_prev"] = df["id"].shift(-1)
df["gen_next"] = df["id"].shift(1)
df["gen_prev_title"] = df["title"].shift(-1)
df["gen_next_title"] = df["title"].shift(1)

for i, ndf in df.groupby("corresp_id"):
    sorted_df = ndf.sort_values("date")
    sorted_df["prev"] = sorted_df["id"].shift(-1)
    sorted_df["next"] = sorted_df["id"].shift(1)
    sorted_df["prev_title"] = sorted_df["title"].shift(-1)
    sorted_df["next_title"] = sorted_df["title"].shift(1)
    print(f"processing thread id {i}")
    for j, x in tqdm(sorted_df.iterrows(), total=len(sorted_df)):
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
        ref.text = f'Korrespondenz mit {x["corresp_names"]}'
        if x["prev"] is not None:
            prevCorr = ET.SubElement(correspContext, 'ref', subtype="previous_letter", type="withinCorrespondence", source=x["corresp_id"], target=x["prev"].split('/')[-1])
            prevCorr.text = "" if x["prev_title"] is None else x["prev_title"].split('/')[-1]
        if x["next"] is not None:
            nextCorr = ET.SubElement(correspContext, 'ref', subtype="next_letter", type="withinCorrespondence", source=x["corresp_id"], target=x["next"].split('/')[-1])
            nextCorr.text = "" if x["next_title"] is None else x["next_title"].split('/')[-1]
        if x["gen_prev"] is not None:
            genPrevCorr = ET.SubElement(correspContext, 'ref', subtype="previous_letter", type="withinCollection", target=x["gen_prev"].split('/')[-1])
            genPrevCorr.text = "" if x["gen_prev_title"] is None else x["gen_prev_title"].split('/')[-1]
        if x["gen_next"] is not None:
            genNextCorr = ET.SubElement(correspContext, 'ref', subtype="next_letter", type="withinCollection", target=x["gen_next"].split('/')[-1])
            genNextCorr.text = "" if x["gen_next_title"] is None else x["gen_next_title"].split('/')[-1]

        doc.tree_to_file(x["id"])

print(f"no date in following {len(non_dateable)} files")
for x in non_dateable:
    print(x)

if broken:
    print(f"the following {len(files)} are not well formed")
    for x in broken:
        print(x)
else:
    print("all files are well formed, good job!")