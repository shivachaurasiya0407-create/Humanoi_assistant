import os
import shutil

src = "platform"
dst = "ai_platform"

if os.path.exists(src):
    if os.path.exists(dst):
        print(f"Destination {dst} already exists. Merging...")
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        shutil.rmtree(src)
    else:
        os.rename(src, dst)
    print("Move complete.")
else:
    print("Source 'platform' not found.")
