# This program intends to make an MD5 list of two folders and save it into a json
# EXPEDIENTES_LLITRA is the actual file
# YACIMIENTO_LLITRA is the file you want to rename
# Comparing MD5, it will rename each document, and if the document is a PDF,
# it will also check if a TXT exists (OCR generated with another tool), and
# update the name of the associated PDF that has just been updated.
import hashlib
import os
import json
import ntpath

CUR_DIR = os.path.dirname(__file__)
EXPEDIENTES_LLITRA_PATH = os.path.join(CUR_DIR, "correct_file.json")
YACIMIENTO_LLITRA_PATH = os.path.join(CUR_DIR, "yacimientos_LLITRA.json")
EXPEDIENTES_LLITRA_FILE = "PATH_TO_OLD_FOLDER/EXPEDIENTES LLITRA"
YACIMIENTO_LLITRA_FILE  = "PATH_TO_NEW_FOLDER/YACIMIENTO_LLITRA"

if os.path.exists(EXPEDIENTES_LLITRA_PATH):
    with open(EXPEDIENTES_LLITRA_PATH, "r") as f:
        new_files = json.load(f)
else:
    new_files = {"new_file_MD5":[], "new_file_name":[], "new_file_path":[]}

if os.path.exists(YACIMIENTO_LLITRA_PATH):
    with open(YACIMIENTO_LLITRA_PATH, "r") as f:
        old_files    =    json.load(f)
else:
    old_files = {"old_file_MD5":[], "old_file_name":[], "old_file_path":[]}

print("Global variables created")

for root, dirs, files in os.walk(EXPEDIENTES_LLITRA_FILE):
    for file in files:
          new_path  = os.path.join(root, file)
          new_name  = ntpath.basename(new_path)
          if ".gsheet" not in new_name:
            new_md5   = hashlib.md5(open(new_path,"rb").read()).hexdigest()

            if new_md5 not in new_files["new_file_MD5"]:
                new_files["new_file_MD5"].append(new_md5)
                new_files["new_file_path"].append(new_path)
                new_files["new_file_name"].append(new_name)

for root, dirs, files in os.walk(YACIMIENTO_LLITRA_FILE):
    for file in files:
          old_path  =    os.path.join(root, file)
          old_name  =    ntpath.basename(old_path)
          if ".gsheet" not in old_name:
            old_md5   =    hashlib.md5(open(old_path,'rb').read()).hexdigest()

            if old_md5 not in old_files["old_file_MD5"]:
                old_files["old_file_MD5"].append(old_md5)
                old_files["old_file_path"].append(old_path)
                old_files["old_file_name"].append(old_name)

with open(EXPEDIENTES_LLITRA_PATH, "w") as f:
     json.dump(new_files, f, indent=4)

with open(YACIMIENTO_LLITRA_PATH, "w") as f:
     json.dump(old_files, f, indent=4)

print("Done.")

i = 0
for old_md5 in old_files["old_file_MD5"]:
     if old_md5 in new_files["new_file_MD5"]:
          ref_new = new_files["new_file_MD5"].index(old_md5)
          pdf_ref_old = old_files["old_file_MD5"].index(old_md5)

          pdf_path2change = old_files["old_file_path"][pdf_ref_old]
          name2change = old_files["old_file_name"][pdf_ref_old]
          pdf_path_changed = pdf_path2change.replace(name2change, "") + new_files["new_file_name"][ref_new]

          if pdf_path2change.endswith(".pdf") and pdf_path2change.replace(".pdf", ".txt") in old_files["old_file_path"]:
               txt_path2change = pdf_path2change[:-4] + ".txt"
               txt_path_changed = pdf_path_changed[:-4] + ".txt"
               os.rename(txt_path2change, txt_path_changed)


          os.rename(pdf_path2change, pdf_path_changed)

     
