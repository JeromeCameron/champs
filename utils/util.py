import os

path = "../pages"

for subdir, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".html"):
            filename = os.path.join(subdir, file)
            os.rename(filename, filename.replace("#", "Event "))
