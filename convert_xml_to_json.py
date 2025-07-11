# Script from Oli (contributor with elfpedia.eu)

import os
import xml.etree.ElementTree as ET
import json
from collections.abc import Mapping

repo_root = os.path.dirname(os.path.abspath(__file__))

xml_folder = os.path.join(repo_root, "raw_game_data", "xml")
template_file1 = os.path.join(repo_root, "templates", "template1.json")
template_file2 = os.path.join(repo_root, "templates", "template2.json")
output_folder = os.path.join(repo_root, "raw_game_data", "json")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def deep_merge(a, b):
    if isinstance(a, Mapping) and isinstance(b, Mapping):
        merged = dict(a)
        for key, val in b.items():
            if key in merged:
                merged[key] = deep_merge(merged[key], val)
            else:
                merged[key] = val
        return merged
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) > 0 and len(b) > 0:
            return [deep_merge(a[0], b[0])]
        elif len(b) > 0:
            return [b[0]]
        else:
            return a
    else:
        return b


def element_to_json(element):
    obj = {}
    if element.attrib:
        obj["_attributes"] = element.attrib
    for child in element:
        tag = child.tag
        child_obj = element_to_json(child)
        if tag in obj:
            if not isinstance(obj[tag], list):
                obj[tag] = [obj[tag]]
            obj[tag].append(child_obj)
        else:
            obj[tag] = child_obj
    text = (element.text or "").strip()
    if text and not obj:
        obj["_text"] = text
    return obj


def merge_template(template, data):
    if isinstance(template, dict) and isinstance(data, dict):
        merged = {}
        for key, value in template.items():
            if key in data:
                merged[key] = merge_template(value, data[key])
            else:
                merged[key] = value
        for key in data:
            if key not in merged:
                merged[key] = data[key]
        return merged
    elif isinstance(template, list):
        if isinstance(data, list) and data:
            return [merge_template(template[0], item) for item in data]
        else:
            return []
    else:
        return data if data != "" else template


def generate_json_filename(xml_root):
    venue = xml_root.find("venue")
    gameid = venue.attrib.get("gameid", "").upper()
    if not gameid or len(gameid) < 8:
        raise ValueError("Missing or invalid gameid.")
    visitor = gameid[0:2].lower()
    home = gameid[2:4].lower()
    season = gameid[4:6]
    round_or_week = gameid[6:].lower()
    return f"{home}{visitor}{season}{round_or_week}.json"


template1 = load_json(template_file1)
template2 = load_json(template_file2)
master_template = deep_merge(template1, template2)

xml_files = [f for f in os.listdir(xml_folder) if f.endswith(".xml")]

for xml_file in xml_files:
    xml_path = os.path.join(xml_folder, xml_file)
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        json_filename = generate_json_filename(root)
        json_path = os.path.join(output_folder, json_filename)

        json_data = {root.tag: element_to_json(root)}
        final_json = merge_template(master_template, json_data)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(final_json, f, indent=2, ensure_ascii=False)

        print(f"✅ Converted {xml_file} → {json_filename}")
    except Exception as e:
        print(f"❌ Error converting {xml_file}: {e}")
