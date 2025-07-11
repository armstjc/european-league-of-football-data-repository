# Script from Oli (contributor with elfpedia.eu)

import os

repo_root = os.path.dirname(os.path.abspath(__file__))
xml_folder = os.path.join(repo_root, "raw_game_data", "xml")
json_folder = os.path.join(repo_root, "raw_game_data", "json")


def parse_xml_filename(filename):
    parts = filename.replace(".xml", "").split("_")
    season = parts[0][2:]
    week = parts[1]
    vis = parts[2].lower()
    home = parts[3].lower()
    suffix = week.lower() if not week.isdigit() else f"{int(week):02d}"
    return f"{home}{vis}{season}{suffix}.json"


xml_files = [f for f in os.listdir(xml_folder) if f.endswith(".xml")]
json_files = set(os.listdir(json_folder))

duplicates = []
xml_only = []

for xml_file in xml_files:
    expected_json = parse_xml_filename(xml_file)
    if expected_json in json_files:
        duplicates.append((xml_file, expected_json))
    else:
        xml_only.append(xml_file)

print("=== Files with both XML and JSON ===")
for xml, js in duplicates:
    print(f"XML: {xml} → JSON: {js}")

print("\n=== Files only existing in XML ===")
for xml in xml_only:
    print(xml)

print(f"\nTotal duplicates: {len(duplicates)}")
print(f"Total XML-only files: {len(xml_only)}")
