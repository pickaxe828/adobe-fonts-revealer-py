from jsoncomment import JsonComment

import shutil
import os
import sys
import subprocess
from tqdm import tqdm

json = JsonComment()

# load reveal_config.json with json
with open("reveal_config.jsonc", "r") as conf_raw:
    conf_raw = conf_raw.read()
    conf = json.loads(conf_raw)

fr = conf["paths"]["from"]
to = conf["paths"]["to"]

# Ensure the user
print(f"Are you sure you would want to copy font files")
print(f"From: {fr}")
print(f"To:   {to}")
if input("(Y/N): ") not in ["y", "Y"]:
    print("Script exited.")
    exit()

print()

# List of ids
fr_files_id = os.listdir(fr)

# Loop through ids and copy them to temp dir
print("Copying files and changing names...")
with tqdm(total=len(fr_files_id), file=sys.stdout) as pbar:
    for file in fr_files_id:
        shutil.copy(os.path.join(fr, file), f"{to}/{file}.otf")

        # Get the font details
        t = subprocess.Popen(
            f"./otfinfo --info {to}/{file}.otf", stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8")

        # Loop through every line
        for i in t.stdout.read().splitlines():
            # Extract the font family name
            if i.find("PostScript name:") != -1:
                # Copy the font from the temp dir to the final dir
                os.replace(f"{to}/{file}.otf", f"{to}/{i.split('     ')[1]}.otf")
                
                # Log
                if conf["log"] == True:
                    pbar.set_description(
                        f"{to}/{file}.otf  ➔  {to}/{i.split('     ')[1]}.otf: \n")

                # Update progress bar
                pbar.update(1)

                break

# Finalize
print(f"\nDone and copied {len(fr_files_id)} files!")
