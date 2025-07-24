# Script from Oli (contributor with elfpedia.eu, GitHub: https://github.com/Kryptator/elf-xml-to-json )

import copy
import json
import os
import xml.etree.ElementTree as ET

repo_root = os.path.dirname(os.path.abspath(__file__))
xml_folder = os.path.join(repo_root, "raw_game_data", "xml")
json_folder = xml_folder  # JSONs landen im gleichen Ordner

template_folder = os.path.join(repo_root, "templates")
template_file1 = os.path.join(template_folder, "template1.json")
template_file2 = os.path.join(template_folder, "template2.json")


# Load JSON templates
def load_json(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


template1 = load_json(template_file1)
template2 = load_json(template_file2)


def xml_attributes(elem):
    return elem.attrib


def parse_team(team_elem):
    """
    Parses a <team> element into a dict.
    """
    team_dict = {"_attributes": team_elem.attrib}

    # Parse <totals>
    totals_elem = team_elem.find("totals")
    if totals_elem is not None:
        totals_dict = {}
        if totals_elem.attrib:
            totals_dict["_attributes"] = totals_elem.attrib

        for child in list(totals_elem):
            child_dict = {"_attributes": child.attrib}
            totals_dict[child.tag] = child_dict

        team_dict["totals"] = totals_dict

    # Find <player> elements under this team
    players = []
    for player_elem in team_elem.findall("player"):
        player_dict = {"_attributes": player_elem.attrib}
        for child in list(player_elem):
            player_dict[child.tag] = {"_attributes": child.attrib}
        players.append(player_dict)

    if players:
        team_dict["player"] = players

    return team_dict


# STEP 1: CONVERT XML → JSON
converted_files = []

for filename in os.listdir(xml_folder):
    if not filename.endswith(".xml"):
        continue

    xml_path = os.path.join(xml_folder, filename)
    json_filename = filename.replace(".xml", ".json")
    json_path = os.path.join(json_folder, json_filename)

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        fbgame_elem = root
        venue_elem = fbgame_elem.find("venue")
        team_elems = fbgame_elem.findall("team")

        venue_attrs = xml_attributes(venue_elem)

        # Map to old field names
        if "visitorid" in venue_attrs:
            venue_attrs["visid"] = venue_attrs.pop("visitorid")
        if "visitor" in venue_attrs:
            venue_attrs["visname"] = venue_attrs.pop("visitor")
        if "home" in venue_attrs:
            venue_attrs["homename"] = venue_attrs.pop("home")

        venue_dict = {"_attributes": venue_attrs}

        teams = []
        for team_elem in team_elems:
            team_dict = parse_team(team_elem)
            teams.append(team_dict)

        json_data = copy.deepcopy(template1)
        json_data["fbgame"]["venue"] = venue_dict
        json_data["fbgame"]["team"] = teams

        # Fill missing keys from template2
        def fill_missing(template_obj, data_obj):
            if isinstance(template_obj, dict):
                for key in template_obj:
                    if key not in data_obj:
                        data_obj[key] = template_obj[key]
                    else:
                        fill_missing(template_obj[key], data_obj[key])
            elif isinstance(template_obj, list):
                # Skip lists
                pass

        fill_missing(template2["fbgame"], json_data["fbgame"])

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        converted_files.append(json_filename)
        print(f"✅ Converted {filename} → {json_filename}")

    except Exception as e:
        print(f"❌ Error converting {filename}: {e}")

print("🎉 Conversion complete.")

# STEP 2: RENAME JSONs TO MATCH REPO NAMING

rename_count = 0

for filename in converted_files:
    old_path = os.path.join(xml_folder, filename)

    try:
        with open(old_path, encoding="utf-8") as f:
            data = json.load(f)

        fbgame = data.get("fbgame", {})
        venue = fbgame.get("venue", {})
        attrs = venue.get("_attributes", {})
        gameid = attrs.get("gameid", "").upper()

        if not gameid or len(gameid) < 8:
            print(f"⚠️ Skipping {filename}: Missing or invalid gameid.")
            continue

        visitor = gameid[0:2].lower()
        home = gameid[2:4].lower()
        season = gameid[4:6]
        round_or_week = gameid[6:].lower()

        # Overwrite naming to match OLD JSONs (Visitor first)
        new_filename = f"{visitor}{home}{season}{round_or_week}.json"

        if new_filename != filename:
            new_path = os.path.join(xml_folder, new_filename)

            if os.path.exists(new_path):
                print(
                    f"⚠️ Skipping rename for {filename}: " +
                    f"target {new_filename} already exists!"
                )
                continue

            os.rename(old_path, new_path)
            print(f"✅ Renamed {filename} → {new_filename}")
            rename_count += 1

    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")

print(f"\nTotal files renamed in xml-folder: {rename_count}")
