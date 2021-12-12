from jsoncomment import JsonComment

import shutil
import os
import subprocess
from tqdm import tqdm

json = JsonComment()

# load reveal_config.json with json
with open("reveal_config.json", "r") as conf_raw:
    conf_raw = conf_raw.read()
    conf = json.loads(conf_raw)

fr = conf["paths"]["from"]
to = conf["paths"]["to"]

# Ensure the user
print(f"Are you sure:")
print(f"From: {fr}")
print(f"To:   {to}")
if input("(Y/N): ") not in ["y", "Y"]:
    print("Script ended.")
    exit()

print()
print("Initializing...")

# List of ids
fr_files_id = os.listdir(fr)

# Try to make temp dir
try:
    os.mkdir("temp")
except:
    pass

# Loop through ids and copy them to temp dir
print("Copying files and changing names...")
for file in tqdm(fr_files_id):
    shutil.copy(os.path.join(fr, file), f"./temp/{file}.otf")

    # Get the font details
    t = subprocess.Popen(
        f"./otfinfo --info ./temp/{file}.otf", stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8")

    # Loop through every line
    for i in t.stdout.read().splitlines():
        # Extract the font family name
        if i.find("PostScript name:") != -1:
            # Copy the font from the temp dir to the final dir
            shutil.copy(f"./temp/{file}.otf", f"{to}/{i.split('     ')[1]}.otf")
            break

# Remove the temp file
print("Removing temp dir...")
shutil.rmtree("./temp")
