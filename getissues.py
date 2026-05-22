import os
import shutil
import zipfile

project_list = [
    "PR13128", "PR17647", "PR18198", "PR18762",
    "PR18772", "PR18773", "PR18838", "PR23978",
    "PR24457", "PR30602", "PR32891", "PR34007",
]

base_network_path = r""
output_root = r"C:\temp\projects_output"
zip_path = r"C:\temp\projects.zip"

os.makedirs(output_root, exist_ok=True)

created_projects = []

for project in project_list:
    source_path = os.path.join(base_network_path, project, "ISSUE")

    if not os.path.exists(source_path):
        print(f"Skipping {project} (no ISSUE folder)")
        continue

    dest_project_folder = os.path.join(output_root, project)
    os.makedirs(dest_project_folder, exist_ok=True)

    for file in os.listdir(source_path):
        src_file = os.path.join(source_path, file)
        dst_file = os.path.join(dest_project_folder, file)

        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)

    created_projects.append(dest_project_folder)
    print(f"Copied: {project}")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for folder in created_projects:
        for root, dirs, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)

                # keep folder structure in zip
                arcname = os.path.relpath(full_path, output_root)

                zipf.write(full_path, arcname)

print(f"\n ZIP created at: {zip_path}")