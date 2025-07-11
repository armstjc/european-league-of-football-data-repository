import os
import shutil

repo_root = os.path.dirname(os.path.abspath(__file__))
xml_folder = os.path.join(repo_root, "raw_game_data", "xml")
duplicates_folder = os.path.join(xml_folder, "duplicates")

os.makedirs(duplicates_folder, exist_ok=True)

# Fill this list with duplicates:
duplicates_xml_files = [
    "2021_06_BT_BD.xml",
    "2021_08_HD_FG.xml",
    # etc.
]

for file in duplicates_xml_files:
    src = os.path.join(xml_folder, file)
    dst = os.path.join(duplicates_folder, file)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {file} → duplicates folder.")