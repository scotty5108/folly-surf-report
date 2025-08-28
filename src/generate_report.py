import os

os.makedirs("site", exist_ok=True)

with open("site/report.txt", "w") as f:
    f.write("This is a test surf report.\nAll systems go! 🌊")
