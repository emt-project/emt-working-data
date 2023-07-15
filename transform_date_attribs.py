import glob
import re
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm


base_path = "./data/work-in-progress/"
file_filter = "*.xml"
irregularAttribs = ["year", "month", "day"]


def containsIsoDateInWhen(date_node):
    when = date_node.get("when")
    if when is None:
        return False
    else:
        return bool(re.match("^\d{4}-\d{2}-\d{2}$", when.strip()))


def standardizeDates(date_node):
    day = date_node.attrib["day"]
    month = date_node.attrib["month"]
    year = date_node.attrib["year"]
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"


def removeIrregularAttribs(date_node):
    for attribName in irregularAttribs:
        if attribName in date_node.attrib:
            _ = date_node.attrib.pop(attribName)


if __name__ == "__main__":
    files = sorted(glob.glob(base_path + "**/" + file_filter, recursive=True))
    for file_path in tqdm(files, total=len(files)):
        try:
            doc = TeiReader(file_path)
        except Exception as e:
            print(f"Bad XML: {file_path}")
            continue
        date_list = doc.any_xpath("//tei:body//tei:date")
        for date in date_list:
            if not containsIsoDateInWhen(date):
                date.attrib["when"] = standardizeDates(date)
            removeIrregularAttribs(date)
            date.attrib["type"] = "letter"
        doc.tree_to_file(file_path)
