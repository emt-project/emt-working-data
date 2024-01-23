import glob
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import normalize_string
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "de_AT")

files = sorted(glob.glob("./data/work-in-progress/*/*.xml", recursive=True))

for x in files:
    try:
        doc = TeiReader(x)
    except:
        continue
    for item in doc.any_xpath(
        ".//tei:correspAction[@type='sent']//tei:date[1][@when-iso]"
    ):
        input_date = datetime.strptime(item.attrib["when-iso"], "%Y-%m-%d")
        output_date_string = normalize_string(input_date.strftime("%A, %e. %B %Y"))
        item.text = output_date_string
    doc.tree_to_file(x)
