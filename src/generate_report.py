import os

# Make sure the output directory exists
os.makedirs("site", exist_ok=True)

# Create a simple test report
with open("site/report.txt", "w") as f:
    f.write("🌊 Hello from Waxfoot Willy!\nThis is a test surf report.")
