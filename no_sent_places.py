import glob
import pandas as pd
from acdh_tei_pyutils.tei import TeiReader


files = sorted(glob.glob("./data/*/*/*.xml"))

data = []
for x in files:
    doc = TeiReader(x)
    for y in doc.any_xpath(".//tei:correspAction[@type='sent']/tei:placeName"):
        ref = y.attrib["ref"]
        data.append([x, ref, y.text])

pd.DataFrame(data, columns=["file", "ref", "name"]).to_csv(
    "sent_places.csv", index=False
)
